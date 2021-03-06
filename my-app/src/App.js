import React, { Component } from "react";
import "./App.css";
import "./Design.css";
import ScrollToBottom from "react-scroll-to-bottom";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import { isLabelWithInternallyDisabledControl } from "@testing-library/user-event/dist/utils";
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

ChartJS.defaults.color = "#c2bbba";
ChartJS.defaults.borderColor = "#c2bbba";

export default class App extends Component {
  state = {
    text: "",
    cart: [],
    Angry: 0,
    Disgust: 0,
    Excited: 0,
    Happy: 0,
    Neutral: 0,
    Sad: 0,
    Surprise: 0,
    emotion_values: [0, 0, 0, 0, 0, 0, 0],
    bool: false,
    maxindex: 0,
  };

  argMax = (array) => {
    return array
      .map((x, i) => [x, i])
      .reduce((r, a) => (a[0] > r[0] ? a : r))[1];
  };

  labels = [
    "Angry",
    "Disgust",
    "Excited",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise",
  ];

  fetchdata = async () => {
    fetch("http://127.0.0.1:8000/twitch/", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: this.state.cart }),
    })
      .then((response) => response.json())
      .then(async (data) => {
        console.log(data["response"]);
        console.log(data["response"]["Angry"]);
        let { Angry, Disgust, Excited, Sad, Surprise, Happy, Neutral } =
          this.state;
        await this.setState({
          Angry: data["response"]["Angry"] || 0,
          Disgust: data["response"]["Disgust"] || 0,
          Excited: data["response"]["Excited"] || 0,
          Sad: data["response"]["Sad"] || 0,
          Neutral: data["response"]["Neutral"] || 0,
          Happy: data["response"]["Happy"] || 0,
          Surprise: data["response"]["Surprise"] || 0,
        });

        await this.setState({
          emotion_values: [
            this.state.Angry,
            this.state.Disgust,
            this.state.Excited,
            this.state.Happy,
            this.state.Neutral,
            this.state.Sad,
            this.state.Surprise,
          ],
        });
        await this.setState({
          maxindex: this.argMax(this.state.emotion_values),
        });
        await this.setState({ bool: true });

        console.log("current state is " + JSON.stringify(this.state));
      });
  };

  saveInput = (e) => {
    this.setState({ text: e.target.value });
  };

  addNewItem = (e) => {
    let { cart, text } = this.state;
    cart.push(text);
    if (cart.length > 0) {
      this.fetchdata();
    }

    this.setState({ text: "" });
    e.preventDefault();
    //this.dummy.current.scrollIntoView({behavior:'smooth'})
  };

  options = {
    plugins: {
      legend: {
        labels: {
          font: {
            size: 16,
          },
        },
      },
    },
    scales: {
      x: {
        ticks: {
          font: {
            size: 14,
          },
        },
        grid: {
          display: false,
        },
      },
      y: {
        ticks: {
          font: {
            size: 14,
          },
        },
        grid: {
          display: false,
        },
      },
    },
  };
  render() {
    return (
      <>
        <div className="outerContainer">
          <div className="container">
            <div className="infoBar">
              <div className="leftInnerContainer">
                <h3>Twitch Chat</h3>
              </div>
            </div>
            <ScrollToBottom className="messages">
              {this.state.cart.map((subItems, sIndex) => (
                <div key={sIndex}>
                  <div className="messageContainer justifyEnd">
                    <div className="messageBox backgroundBlue">
                      <p className="messageText colorWhite">{subItems}</p>
                    </div>
                  </div>
                </div>
              ))}
            </ScrollToBottom>
            <form className="form">
              <input
                className="input"
                type="text"
                placeholder="Type your comment..."
                value={this.state.text}
                onChange={this.saveInput}
              />
              <button
                className="sendButton"
                onClick={this.addNewItem}
                style={{ cursor: "pointer" }}
              >
                Send
              </button>
            </form>
          </div>
          {this.state.bool && (
            <div className="col-6 textContainer">
              <Bar
                data={{
                  labels: this.labels,
                  datasets: [
                    {
                      label: "Emotions identified",
                      data: this.state.emotion_values,
                      backgroundColor: this.state.emotion_values.map(
                        (v, index) =>
                          index === this.state.maxindex ? "#ed6a1f" : "#1fafed"
                      ),
                    },
                  ],
                }}
                options={this.options}
              />
            </div>
          )}
        </div>
      </>
    );
  }
}
