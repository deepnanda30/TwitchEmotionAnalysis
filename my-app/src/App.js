import React, { Component } from "react";
import "./App.css";
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
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

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
    maxindex:0,
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
    fetch("http://127.0.0.1:8000/twitch/",{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body:JSON.stringify({"message":this.state.cart})
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

        
       await  this.setState({
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
          maxindex:this.argMax(this.state.emotion_values)
        })
        await this.setState({ bool: true });
       
       
        console.log("current state is "+ JSON.stringify(this.state) );
        
      });
  };

  saveInput = (e) => {
    this.setState({ text: e.target.value });
  };

  addNewItem = (e) => {
    let { cart, text } = this.state;
    cart.push(text);
    if (cart.length > 1) {
      this.fetchdata();
    }

    this.setState({ text: "" });
    e.preventDefault();
    this.dummy.current.scrollIntoView({behavior:'smooth'})
  };

  render() {
    return (
      <div className="row">
        {/* chart */}
        <div className="col-6 form-group">
          <form>
            <div className="form-group p-2 ">
              <label for="exampleInputEmail1" className="p-2">
                Twitch Chat Box
              </label>
              <div className="col-sm-6">
                <input
                  className="form-control "
                  aria-describedby="emailHelp"
                  placeholder="Enter text"
                  value={this.state.text}
                  type="text"
                  onChange={this.saveInput}
                />
              </div>

              <small id="emailHelp" className="form-text text-muted"></small>
            </div>
            <div className="p-2">
              <button onClick={this.addNewItem} className="btn btn-primary ">
                {" "}
                Add Comment{" "}
              </button>
            </div>
            <ol>
              {this.state.cart.map((subItems, sIndex) => {
                return <li key={sIndex}> {subItems}</li>;
              })}
            </ol>
          </form>
        </div>


        {/* chart */}
        {this.state.bool && (
        <div className="col-6">
          <Bar
            data= {
              {labels: this.labels,
              datasets: [
                {
                  label: "Emotions identified",
                  data: this.state.emotion_values,
                  backgroundColor: this.state.emotion_values.map((v, index) =>
                  index === this.state.maxindex ? "#ed6a1f" : "#1fafed"
                ),
                },
              ]}
            }
            
          />
        </div>
        )}
      </div>
    );
  }
}
