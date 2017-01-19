import React from 'react';
import ReactDOM from 'react-dom';

import Datepicker from './components/Datepicker.jsx';
import Charts from './components/Charts.jsx'

import DatesStore from './stores/DatesStore.jsx'
import DashboardActions from './DashboardActions.jsx';

DashboardActions.loadProjectsData();

class Dashboard extends React.Component {
    constructor(){
        super();
        this.state = DatesStore.getDates();
    }

    componentWillMount () {
        DatesStore.on('update', () => {
            this.setState(DatesStore.getDates());
        });
    }

    render() {
        return (
            <div className="dashboard">
                <div className="dashboard__header">
                    <h1 className="dashboard__title">Redwerk Dashboard</h1>
                    <Datepicker startDate={this.state.startDate} endDate={this.state.endDate} />
                </div>
                <Charts />
            </div>
        );
    }
}

ReactDOM.render(
    <Dashboard />,
    document.getElementById('container')
);