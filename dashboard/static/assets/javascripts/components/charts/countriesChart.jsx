import React from 'react';
import {Doughnut} from 'react-chartjs-2';
import DashboardActions from '../../DashboardActions.jsx';
import ProjectStore from '../../stores/ProjectStore.jsx';


class chartSettings {
    constructor(labels, data){
      this.labels = labels;

      this.datasets = [{
          data: data,
          backgroundColor: [
            '#6CD0EA',
            '#FFDE7D',
            '#FE9ABE',
            '#4AAF5F',
            '#E63C3C'
          ],
          hoverBackgroundColor: [
            '#6CD0EA',
            '#FFDE7D',
            '#FE9ABE',
            '#4AAF5F',
            '#E63C3C'
          ]
      }]
    }
}
export default class CountriesChart extends React.Component {
     constructor(props){
        super(props);
        this._options = {
            legend: {
                position: 'right',
                fontSize: '22',
                padding: '20px',
                boxWidth: 10
            }
        };
        this.state = {
            statesActive: false,
            statesData: ProjectStore.getStatesData()
        }
     }

     handleElementsClick(elems) {
         DashboardActions.selectCountry(elems[0]._index)
     }

     handleBackToCountries(){
         this.setState({
             statesActive: false
         })
     }

     componentWillMount() {
         ProjectStore.on("updateStatesData", () => {
             this.setState({
                  statesData: ProjectStore.getStatesData(),
                  statesActive: true,
             });
         });
     }

     render() {

        return <div className={"chart " + (this.state.statesActive ? "chart--two" : null)}>
                <div className="chart__wrapper">
                    <div className="chart__header">
                        <h3 className="chart__title">Countries</h3>
                    </div>
                    <div className="chart__container">
                        <Doughnut data={new chartSettings(this.props.labels, this.props.data)} options={this._options}
                                  onElementsClick={this.handleElementsClick.bind(this)} redraw={true} />
                    </div>
                </div>
                {this.state.statesData.labels.length ?
                <div className="chart__wrapper">
                    <div className="chart__header">
                        <h3 className="chart__title">States</h3>
                        <div className="chart__back" onClick={this.handleBackToCountries.bind(this)}>Back</div>
                    </div>
                    <div className="chart__container">
                         <Doughnut data={new chartSettings(this.state.statesData.labels, this.state.statesData.data)}
                                   options={this._options} redraw={true} />
                    </div>
                </div>
                    : null}
            </div>;


     }
}



CountriesChart.defaultProps = {};
CountriesChart.propTypes = {};