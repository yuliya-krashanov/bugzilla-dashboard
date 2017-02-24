import { EventEmitter } from 'events';
import 'whatwg-fetch';
import dispatcher from '../DashboardDispatcher.jsx';
import DatesStore from './DatesStore.jsx';
import ActionTypes from '../constants/ActionTypes.jsx';
import { formatDataForCharts } from '../DashboardUtils.js';


class ProjectStore extends EventEmitter {
    constructor() {
        super();
        this.projectsData = {};
        this.chartProjectsData = {
            projects: {
                 labels: [], data: []
            },
            countries: {
                 labels: [], data: []
            }};
        this.statesData = { labels: [], data: [] };
    }

    projectDataLoaded (data) {
        this.projectsData = data;
        for (let items in this.projectsData){
            if (this.projectsData.hasOwnProperty(items))
                this.chartProjectsData[items] = formatDataForCharts(this.projectsData[items])
        }
        this.emit('updateProjectData');
    }

    statesDataLoaded (data) {
        this.statesData = formatDataForCharts(data);
        this.emit('updateStatesData');
    }

    loadProjectsData (){
        fetch('api/projects', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(DatesStore.getFormatDates()),

        })
            .then((response) => {
                return response.json();
            })
            .then( (data) => {
                this.projectDataLoaded(data);
            })
            .catch( console.log );
    }

    loadStatesData (country){
        fetch('api/states', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify( Object.assign( DatesStore.getFormatDates(),
                {
                    countryID: this.projectsData.countries[country].id
                })),

        })
        .then((response) => {
            return response.json();
        })
        .then( (data) => {
            this.statesDataLoaded(data);
        })
        .catch( console.log );
    }

    getChartProjectsData() {
        return this.chartProjectsData;
    }

    getProjectsData() {
        return this.projectsData;
    }

    getStatesData() {
        return this.statesData;
    }

    handleActions (action) {
        switch (action.type){
            case ActionTypes.LOAD_PROJECTS_DATA:
                this.loadProjectsData();
                break;
            case ActionTypes.SELECT_COUNTRY:
                this.loadStatesData(action.countryID);
                break;
            case ActionTypes.CHANGE_DATES:
                // TODO: fix waitFor in event listener
                /*dispatcher.waitFor([
                     DatesStore.dispatchToken
                ]);*/
                this.loadProjectsData();

        }
    }
}

const projectStore = new ProjectStore();
ProjectStore.dispatchToken = dispatcher.register(projectStore.handleActions.bind(projectStore))

export default projectStore;