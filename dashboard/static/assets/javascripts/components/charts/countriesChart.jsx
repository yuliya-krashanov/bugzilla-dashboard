import React from 'react';
import {Doughnut} from 'react-chartjs-2';
import DashboardActions from '../../DashboardActions.jsx';
import ProjectStore from '../../stores/ProjectStore.jsx';
import {chartSettings} from '../../DashboardUtils.js';

export default class CountriesChart extends React.Component {
     constructor(props){
        super(props);

        this.redrawCountry = true;

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

     componentWillUpdate(nextProps, nextState){
        if (nextProps.data == this.props.data)
            this.redrawCountry = false;
     }

     render() {

        const countryChartSettings = new chartSettings(this.props.labels, this.props.data);
        const statesChartSettings = new chartSettings(this.state.statesData.labels, this.state.statesData.data);

        return <div className={"chart " + (this.state.statesData.labels.length ? "chart--two " : null)
                + (this.state.statesActive ? "chart--states-active " : null)}>
                <div className="chart__wrapper">
                    <div className="chart__header">
                        <h3 className="chart__title">Countries</h3>
                    </div>
                    <div className="chart__container">
                        <Doughnut data={{datasets: countryChartSettings.datasets, labels: countryChartSettings.labels}}
                                  options={countryChartSettings.options}
                                  onElementsClick={this.handleElementsClick.bind(this)} redraw={this.redrawCountry} />
                    </div>
                </div>
                {this.state.statesData.labels.length ?
                    <div className="chart__wrapper">
                        <div className="chart__header">
                            <h3 className="chart__title">States</h3>
                            <div className="chart__button chart__button--back" onClick={this.handleBackToCountries.bind(this)}>
                                <img src={"static/public/images/downwards-pointer.svg"} alt="back"/>
                                 Back
                            </div>
                        </div>
                        <div className="chart__container">
                             <Doughnut data={{datasets: statesChartSettings.datasets, labels: statesChartSettings.labels}}
                                       options={statesChartSettings.options} redraw={true} />
                        </div>
                    </div>
                : null}
            </div>;
     }
}

CountriesChart.defaultProps = {};
CountriesChart.propTypes = {};