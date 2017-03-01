import { EventEmitter } from 'events';
import 'whatwg-fetch';
import dispatcher from '../DashboardDispatcher.jsx';
import DatesStore from './DatesStore.jsx';
import ProjectStore from './ProjectStore.jsx';
import ActionTypes from '../constants/ActionTypes.jsx';
import {formatDataForCharts, encodeGETQuery} from '../DashboardUtils.js'

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
        this.chartData =  formatDataForCharts(this.detailsData);
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
         const params = {
            startDate: DatesStore.getFormatStartMonth(),
            projectID: this.projectID,
            period: this.periods[this.activePeriod],
         };

         fetch('api/details/' + encodeGETQuery(params), {
            headers: {
              'Accept': 'application/json'
            }
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

    closeChart() {
        this.emit("close");
    }

    handleActions (action) {
        switch (action.type){
            case ActionTypes.SELECT_PROJECT:
                this.changeProject(action.iterator);
                break;
            case ActionTypes.CHANGE_DATES:
                this.closeChart();
                break;
            case ActionTypes.CHANGE_PERIOD:
                this.changePeriod(action.increase);
        }

    }
}


const detailStore = new DetailStore();
DetailStore.dispatchToken = dispatcher.register(detailStore.handleActions.bind(detailStore))

export default detailStore;