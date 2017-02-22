import React from 'react';
import DateRangePicker from 'react-bootstrap-daterangepicker';
import DatesStore from '../stores/DatesStore.jsx';
import DashboardActions from '../DashboardActions.jsx'

export default class Datepicker extends React.Component {
    constructor(){
        super();
        this.state = DatesStore.getDates();
    }

    handleChangeDate(e, picker) {
        DashboardActions.changeDate(picker.startDate, picker.endDate)
    }

    componentWillMount () {
        DatesStore.on('update', () => {
            this.setState(DatesStore.getDates());
        });
    }

    render() {
        const startDateFormat = this.state.startDate.year() === this.state.endDate.year() ? 'MMM D' : 'MMM D, Y';

        return (
            <div className="datepicker">
                <DateRangePicker startDate={this.state.startDate} endDate={this.state.endDate} onApply={this.handleChangeDate}>
                    <input type="text" disabled
                           value={this.state.startDate.format(startDateFormat) + ' - ' + this.state.endDate.format('MMM D, Y')}  />
                    <div className="datepicker__arrow"></div>
                </DateRangePicker>
            </div>
            );
    }
}