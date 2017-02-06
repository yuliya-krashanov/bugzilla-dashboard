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
                    <span>
                        <svg version="1.1" x="0px" y="0px"
                             viewBox="0 0 201.5 201.5">
                            <g>
                                <path d="M193.2,46.3l8.3,8.3L100.7,155.3L0,54.5l8.3-8.3l92.5,92.5L193.2,46.3z"/>
                            </g>
                        </svg>
                    </span>
                </DateRangePicker>
            </div>
            );
    }
}

Datepicker.defaultProps = {};
Datepicker.propTypes = {};