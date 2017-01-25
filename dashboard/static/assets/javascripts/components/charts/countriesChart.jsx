import React from 'react';
import {Doughnut} from 'react-chartjs-2';
import DashboardActions from '../../DashboardActions.jsx';
import ProjectStore from '../../stores/ProjectStore.jsx';
import {chartSettings, PieChartOptions} from '../../DashboardUtils.js';

export default class CountriesChart extends React.Component {
     constructor(props){
        super(props);

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

        return <div className={"chart " + (this.state.statesData.labels.length ? "chart--two " : null)
                + (this.state.statesActive ? "chart--states-active " : null)}>
                <div className="chart__wrapper">
                    <div className="chart__header">
                        <h3 className="chart__title">Countries</h3>
                    </div>
                    <div className="chart__container">
                        <Doughnut data={new chartSettings(this.props.labels, this.props.data)} options={PieChartOptions}
                                  onElementsClick={this.handleElementsClick.bind(this)} redraw={true} />
                    </div>
                </div>
                {this.state.statesData.labels.length ?
                    <div className="chart__wrapper">
                        <div className="chart__header">
                            <h3 className="chart__title">States</h3>
                            <span className="chart__button chart__button--back" onClick={this.handleBackToCountries.bind(this)}>
                                <i className="fa fa-angle-left"></i> Back
                            </span>
                        </div>
                        <div className="chart__container">
                             <Doughnut data={new chartSettings(this.state.statesData.labels, this.state.statesData.data)}
                                       options={PieChartOptions} redraw={true} />
                        </div>
                    </div>
                : null}
            </div>;
     }
}

CountriesChart.defaultProps = {};
CountriesChart.propTypes = {};