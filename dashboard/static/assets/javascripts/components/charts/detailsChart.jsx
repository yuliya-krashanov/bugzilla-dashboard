import React from 'react';
import {Bar} from 'react-chartjs-2';
import DashboardActions from '../../DashboardActions.jsx'
import DetailStore from '../../stores/DetailStore.jsx';


export default class DetailsChart extends React.Component {
     constructor(props){
        super(props);

        this._periods = {
            month: 'Daily',
            year: 'Annual'
        };

        this.statistics = {
            min: 0,
            max: 0,
            avg: 0
        };

        this.state = {
            hidden: true,
            name: DetailStore.projectName,
            details: DetailStore.getChartData(),
            period: this._periods[DetailStore.getCurrentPeriod()]
        }

     }

     componentWillMount() {

         DetailStore.on("update", () => {
             this.setState({
                 hidden: false,
                 details: DetailStore.getChartData(),
                 name: DetailStore.projectName,
                 period: this._periods[DetailStore.getCurrentPeriod()]
             })
         });
     }

     handleClose() {
         this.setState({
             hidden: true
         })
     }

     countStatistics(){
         this.statistics = {
             min: Math.min.apply(Math, this.state.details.data),
             max: Math.max.apply(Math, this.state.details.data),
             avg: Math.round(this.state.details.data.reduce(function (a, b) {
                 return a + b;
             }) / this.state.details.data.length)
         };
     }

     handleDecreasePeriod() {
        DashboardActions.changePeriod(false);
     }

     handleIncreasePeriod() {
        DashboardActions.changePeriod(true);
     }

     render() {
        if (!this.state.hidden){

            const data = {
              labels:  this.state.details.labels,
              datasets: [
                {
                  label: '',
                  backgroundColor: 'rgba(255,99,132,0.2)',
                  borderColor: 'rgba(255,99,132,1)',
                  borderWidth: 1,
                  hoverBackgroundColor: 'rgba(255,99,132,0.4)',
                  hoverBorderColor: 'rgba(255,99,132,1)',
                  data: this.state.details.data
                }
              ]
            };

            this.countStatistics();

            return <div className="chart chart--details">
                  <div className="chart__header">
                      <div className="chart__titles">
                          <h3 className="chart__title">{this.state.name}</h3>
                          <h5 className="chart__subtitle">{this.state.period} statistics of working hours</h5>
                      </div>
                      <button className="chart__button chart__button--close" onClick={this.handleClose.bind(this)}>x</button>

                  </div>

                  <Bar data={data}
                      options={{
                        maintainAspectRatio: true,
                          legend: {
                            position: 'none'
                          }
                      }}
                  />

                  <div className="settings">
                      <div className="settings__zoom">
                        <button className="settings__button" onClick={this.handleDecreasePeriod}>-</button>
                        <button className="settings__button" onClick={this.handleIncreasePeriod}>+</button>
                      </div>
                      <div className="stats">
                          <div className="stats__item">Min hours a day<span> {this.statistics.min}</span></div>
                          <div className="stats__item">Max hours a day<span> {this.statistics.max}</span></div>
                          <div className="stats__item">Avg hours a day<span> {this.statistics.avg}</span></div>
                      </div>
                  </div>
            </div>;
        }
        else return null;

     }
}

DetailsChart.defaultProps = {};
DetailsChart.propTypes = {};