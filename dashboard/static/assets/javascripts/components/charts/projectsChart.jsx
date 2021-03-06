import React from 'react';
import DashboardActions from '../../DashboardActions.jsx'
import {Doughnut} from 'react-chartjs-2';
import {chartSettings} from '../../DashboardUtils.js';


export default class ProjectsChart extends React.Component {
     constructor(props){
        super(props);
     }

     handleElementsClick (elems){
        DashboardActions.selectProject(elems[0]._index);
     }

     render() {

         const projectChartSettings = new chartSettings(this.props.labels, this.props.data);

         return <div className="chart">
             <div className="chart__wrapper">
                 <div className="chart__header">
                     <h3 className="chart__title">Projects</h3>
                 </div>
                 <div className="chart__container">
                     {this.props.labels.length ?
                         <Doughnut data={{datasets: projectChartSettings.datasets, labels: projectChartSettings.labels}}
                                   redraw={true} options={projectChartSettings.options}
                                   onElementsClick={this.handleElementsClick.bind(this)}/>
                         : 'No data for these dates!'}
                 </div>
             </div>
         </div>;
     }
}

ProjectsChart.defaultProps = {};