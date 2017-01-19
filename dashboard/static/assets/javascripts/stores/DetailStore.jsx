import { EventEmitter } from 'events';
import 'whatwg-fetch';
import dispatcher from '../DashboardDispatcher.jsx';
import DatesStore from './DatesStore.jsx';
import ProjectStore from './ProjectStore.jsx';
import ActionTypes from '../constants/ActionTypes.jsx';

class DetailStore extends EventEmitter {

    constructor() {
        super();
        this.detailsData = [];
        this.periods = ['year', 'month'];
        this.activePeriod = 1;
        this.projectID = 0;
        this.projectName = '';
        this.chartData = [];
    }

    dataLoaded (data) {
        this.detailsData = data;
        this.chartData =  this.detailsData.reduce((fin, item) => {
                 fin.labels.push(item.label);
                 fin.data.push(item.data);
                 return fin;
             }, { labels: [], data: [] });

        this.emit('update');
    }

    changeProject(iterator) {
        this.projectID = ProjectStore.getProjectsData().projects[iterator].id;
        this.projectName = ProjectStore.getProjectsData().projects[iterator].name;
        this.updateData();
    }

    changePeriod(increase){
        const prevValue = this.activePeriod;
        this.activePeriod = increase ?
            ( (this.activePeriod + 1) >= this.periods.length ? this.activePeriod : this.activePeriod + 1) :
            ( (this.activePeriod - 1) < 0 ? this.activePeriod : this.activePeriod - 1);
        if (prevValue !== this.activePeriod) this.updateData();
    }

    updateData() {
         fetch('api/details', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify( Object.assign({startDate: DatesStore.getFormatStartMonth()},
                    {
                        projectID: this.projectID,
                        period: this.periods[this.activePeriod]
                    }))
         })
         .then( (response) => {
            return response.json();
         })
         .then( (data) => {
            this.dataLoaded(data);
         })
         .catch( console.log );
    }

    getCurrentPeriod (){
        return this.periods[this.activePeriod];
    }

    getData() {
        return this.detailsData;
    }

    getChartData() {
        return this.chartData;
    }

    handleActions (action) {
        switch (action.type){
            case ActionTypes.SELECT_PROJECT:
                this.changeProject(action.iterator);
                break;
            case ActionTypes.CHANGE_PERIOD:
                this.changePeriod(action.increase);
        }

    }
}


const detailStore = new DetailStore();
DetailStore.dispatchToken = dispatcher.register(detailStore.handleActions.bind(detailStore))

export default detailStore;