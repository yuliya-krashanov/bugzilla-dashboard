import React from 'react';
import DashboardActions from '../../DashboardActions.jsx'
import {Doughnut} from 'react-chartjs-2';


export default class ProjectsChart extends React.Component {
     constructor(props){
        super(props);

        this._options =  {
            legend: {
                position: 'right'
            }
        };
     }

     handleElementsClick (elems){
        DashboardActions.selectProject(elems[0]._index);
     }

     render() {

         const data = {
             labels: this.props.labels,
             datasets: [{
                 data: this.props.data,
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
         };

         return <div className="chart">
             <div className="chart__wrapper">
                 <div className="chart__header">
                     <h3 className="chart__title">Projects</h3>
                 </div>
                 <div className="chart__container">
                     { data.labels.length ?
                         <Doughnut data={data} redraw={true} options={this._options}
                                   onElementsClick={this.handleElementsClick.bind(this)}/>
                         : 'No data for these dates!'}
                 </div>
             </div>
         </div>;
     }

}

ProjectsChart.defaultProps = {};