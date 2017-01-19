import dispatcher from './DashboardDispatcher.jsx';
import ActionTypes from './constants/ActionTypes.jsx';

export default {

    selectProject(iterator)  {
        dispatcher.dispatch({
            type: ActionTypes.SELECT_PROJECT,
            iterator
        });
    },

    selectCountry(countryID)  {
        dispatcher.dispatch({
            type: ActionTypes.SELECT_COUNTRY,
            countryID
        });
    },

    changeDate(startDate, endDate) {
        dispatcher.dispatch({
            type: ActionTypes.CHANGE_DATES,
            startDate,
            endDate
        });
    },

    loadProjectsData() {
        dispatcher.dispatch({
            type: ActionTypes.LOAD_PROJECTS_DATA
        });
    },

    loadStatesData(countryID) {
        dispatcher.dispatch({
            type: ActionTypes.LOAD_STATES_DATA,
            countryID
        });
    },

    changePeriod(increase) {
        dispatcher.dispatch({
            type: ActionTypes.CHANGE_PERIOD,
            increase
        });
    }
}