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

         DetailStore.on("close", () => {
             this.handleClose();
         });
     }

     handleClose() {
         this.setState({
             hidden: true
         })
     }

     countStatistics(){
         let positiveData = this.state.details.data.filter(item => {return item > 0;});
         if (positiveData.length)
             this.statistics = {
                 min: Math.min.apply(Math, positiveData),
                 max: Math.max.apply(Math, positiveData),
                 avg: Math.round(positiveData.reduce(function (a, b) {
                     return a + b;
                 }) / positiveData.length)
             };
         else
             this.statistics = {
                min: 0,
                max: 0,
                avg: 0
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
                  backgroundColor: '#F5AEAC',
                  borderColor: '#F5AEAC',
                  borderWidth: 0,
                  hoverBackgroundColor: '#DD3333',
                  hoverBorderColor: '#DD3333',
                  data: this.state.details.data
                }
              ]
            };

            this.countStatistics();

            return <div className="chart chart--details">
                <div className="chart__wrapper">
                  <div className="chart__header">
                      <div className="chart__titles">
                          <h3 className="chart__title">{this.state.name}</h3>
                          <h5 className="chart__subtitle">{this.state.period} statistics of working hours</h5>
                      </div>
                      <div className="chart__button chart__button--close" onClick={this.handleClose.bind(this)}>
                           <img src={"static/public/images/cross-out.svg"} alt="close" />
                      </div>
                  </div>

                  <Bar data={data}
                      options={{
                        maintainAspectRatio: true,
                        legend: {
                            position: 'none'
                        },
                        tooltips: {
                            backgroundColor: 'transparent',
                            bodyFontColor: '#DD3333',
                            bodyFontSize: 25,
                            bodyFontFamily: 'Lato',
                            cornerRadius: 0,
                            displayColors: false,
                            callbacks: {
                                label: (tooltip, data) => {
                                    return `${data.datasets[0].data[tooltip.index]}h`;
                                },
                                title: (tooltip, data) => {
                                    return '';
                                },
                            }
                        },
                        scales: {
                            yAxes: [
                                {
                                    display: false
                                }
                            ],
                            xAxes: [
                                {
                                    gridLines: {
                                        display: false
                                    },
                                    categoryPercentage: 0.5
                                }
                            ],
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
                </div>
            </div>;
        }
        else return null;

     }
}

DetailsChart.defaultProps = {};
DetailsChart.propTypes = {};