import React from 'react';
import DateRangePicker from 'react-bootstrap-daterangepicker';
import DashboardActions from '../DashboardActions.jsx'

export default class Datepicker extends React.Component {
    constructor(props){
        super(props);
    }
    handleChangeDate(e, picker) {
        DashboardActions.changeDate(picker.startDate, picker.endDate)
    }
    render() {
        const startDateFormat = this.props.startDate.year() === this.props.endDate.year() ? 'MMM D' : 'MMM D, Y';
        return (
            <div className="datepicker">
                <DateRangePicker startDate={this.props.startDate} endDate={this.props.endDate} onApply={this.handleChangeDate}>
                    <input type="text" disabled
                           value={this.props.startDate.format(startDateFormat) + ' - ' + this.props.endDate.format('MMM D, Y')}  />
                </DateRangePicker>
            </div>
            );
    }
}

Datepicker.defaultProps = {};
Datepicker.propTypes = {};