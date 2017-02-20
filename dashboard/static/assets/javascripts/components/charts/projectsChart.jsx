import React from 'react';
import DashboardActions from '../../DashboardActions.jsx'
import {Doughnut} from 'react-chartjs-2';
import {chartSettings, PieChartOptions} from '../../DashboardUtils.js';


export default class ProjectsChart extends React.Component {
     constructor(props){
        super(props);
     }

     handleElementsClick (elems){
        DashboardActions.selectProject(elems[0]._index);
     }

     render() {

         return <div className="chart">
             <div className="chart__wrapper">
                 <div className="chart__header">
                     <h3 className="chart__title">Projects</h3>
                 </div>
                 <div className="chart__container">
                     {this.props.labels.length ?
                         <Doughnut data={new chartSettings(this.props.labels, this.props.data)} redraw={true}
                                   options={PieChartOptions} onElementsClick={this.handleElementsClick.bind(this)}/>
                         : 'No data for these dates!'}
                 </div>
             </div>
         </div>;
     }
}

ProjectsChart.defaultProps = {};