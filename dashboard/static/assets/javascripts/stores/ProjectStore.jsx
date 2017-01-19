import { EventEmitter } from 'events';
import 'whatwg-fetch';
import dispatcher from '../DashboardDispatcher.jsx';
import DatesStore from './DatesStore.jsx';
import ActionTypes from '../constants/ActionTypes.jsx';


class ProjectStore extends EventEmitter {
    constructor() {
        super();
        this.projectsData = {};
        this.chartProjectsData = {
            projects: {
                data: [], labels: []
            },
            countries: {
                data: [], labels: []
            }};
        this.statesData = {};
    }

    projectDataLoaded (data) {
        this.projectsData = data;
        this._formatProjectsData();
        this.emit('updateProjectData');
    }

    _formatProjectsData(){
         for (let items in this.projectsData){
            if (this.projectsData.hasOwnProperty(items))
                this.chartProjectsData[items] = this.projectsData[items].reduce((fin, item) => {
                     fin.labels.push(item.name);
                     fin.data.push(item.hours);
                     return fin;
                 }, { labels: [], data: [] });
        }
    }

    statesDataLoaded (data) {
        this.statesData = data;
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

    loadStatesData (){
        fetch('api/states', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify( Object.assign( DatesStore.getFormatDates()),
                    {
                        stateID: this.periods[this.activePeriod]
                    }),

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