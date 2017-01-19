import React from 'react';
import 'whatwg-fetch';
import ProjectChart from './charts/projectsChart.jsx'
import CountriesChart from './charts/countriesChart.jsx'
import DetailsChart from './charts/detailsChart.jsx'

import ProjectStore from '../stores/ProjectStore.jsx';

export default class Charts extends React.Component {
     constructor(){
         super();
         const projectsData = ProjectStore.getChartProjectsData();
         this.state = {
            projects: projectsData.projects,
            countries: projectsData.countries
         };
     }


     componentWillMount() {
         ProjectStore.on("updateProjectData", () => {
             const projectsData = ProjectStore.getChartProjectsData();
             this.setState({
                  projects: projectsData.projects,
                  countries: projectsData.countries,
             });
         });
     }

     render() {
        return  <div className="dashboard__charts">
                    <div className="row">
                        <div className="col-sm-6"><ProjectChart data={this.state.projects.data} labels={this.state.projects.labels} /></div>
                        <div className="col-sm-6"><CountriesChart  data={this.state.countries.data} labels={this.state.countries.labels} /></div>
                    </div>
                    <div className="row">
                        <div className="col-sm-12"><DetailsChart  /></div>
                    </div>
                </div>;
     }
}