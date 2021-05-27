import React from 'react';
import { BrowserRouter as Router, Switch, Route, Link, useParams } from 'react-router-dom';
import BarDetails from './BarDetails';
import BarList from './BarList';

export default () => (
    <Router>
        <div>
            <Switch>
                <Route path="/bar/:bar_name" children={<BarDetails />} />
                <Route path="/" children={<BarList />} />
            </Switch>
        </div>
    </Router>
);
