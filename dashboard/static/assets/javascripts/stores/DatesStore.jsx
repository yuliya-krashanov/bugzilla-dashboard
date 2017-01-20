import { EventEmitter } from 'events';
import moment from 'moment';
import dispatcher from '../DashboardDispatcher.jsx';
import ActionTypes from '../constants/ActionTypes.jsx';

class DatesStore extends EventEmitter {
    constructor() {
        super();
        this.startDate = moment().subtract(2, 'months').startOf('month');
        this.endDate = moment().endOf('month').endOf('day');
    }

    updateDates(startDate, endDate) {
         this.startDate = startDate;
         this.endDate = endDate;
         this.emit('update');
    }

    getDates() {
        return {startDate: this.startDate, endDate: this.endDate};
    }

    getFormatDates() {
        return {startDate: this.startDate.format('D.M.Y'), endDate: this.endDate.format('D.M.Y')};
    }

    getFormatStartMonth() {
        return this.startDate.format('M.Y');
    }

    handleActions (action) {
        switch (action.type){
            case ActionTypes.CHANGE_DATES:
                this.updateDates(action.startDate, action.endDate);
        }
    }
}


const datesStore = new DatesStore();
DatesStore.dispatchToken = dispatcher.register(datesStore.handleActions.bind(datesStore))

export default datesStore;