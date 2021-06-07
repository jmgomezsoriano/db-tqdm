import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const API_URL_BAR_DETAILS = (bar_name) => `/api/bar/${bar_name}`;

export default () => {
    const { bar_name } = useParams();

    const [bar, setBar] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(false);

    useEffect(() => {
        //assign interval to a variable to clear it.
        setError(false);
        setLoading(true);
        fetch(API_URL_BAR_DETAILS(bar_name))
            .then((res) => res.json())
            .then((data) => {
                setBar(data);
                setLoading(false);
            })
            .catch(function (error) {
                console.log(error);
                setError(true);
                setLoading(false);
            });
    }, [bar_name]);

    if (!bar) return <div>No loaded</div>;

    const { desc, percentage, color, n, total, elapsed_str, remaining_str, rate, unit, secondary_unit } = bar;
    return (
        <React.Fragment>
            <h4 className="my-0 fw-normal">{bar_name}</h4>
            <div className="card-body">
                <p>{desc}</p>
                <div className="progress" style={{ height: '30px' }}>
                    <div className="progress-bar progress-bar-striped" role="progressbar"
                        style={{ width: `${parseInt(percentage)}%`, backgroundColor: color }}>
                        {parseInt(percentage)}%
                    </div>
                </div>
                <h2 id="test3-speed" className="card-title pricing-card-title">
                    {rate.toFixed(2)} <span id="test3-primary-unit">{unit}</span>
                    <small className="text-muted fw-light">/{secondary_unit}</small>
                </h2>
                <ul className="list-unstyled mt-3 mb-4">
                    <li>
                        <b>Position:</b> <span>{n}</span>/<span>{total}</span>
                    </li>
                    <li>
                        <b>Elapsed:</b> <span>{elapsed_str}</span>
                    </li>
                    <li>
                        <b>Remain:</b> <span>{remaining_str}</span>
                    </li>
                </ul>
            </div>
        </React.Fragment>
    );
};
