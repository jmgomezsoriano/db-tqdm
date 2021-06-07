import React from 'react';
import { Link } from 'react-router-dom';

export default ({ onClose, bar_name, desc, percentage, color, n, total, elapsed_str, remaining_str, rate, unit, secondary_unit }) => (
    <div id={bar_name} className="col">
        <div className="card mb-4 rounded-3 shadow-sm">
            <div className="card-header py-3">
                <h4 className="my-0 fw-normal">{bar_name}</h4>
            </div>
            <div className="card-body">
                <p>{desc}</p>
                <div className="progress" style={{ height: '30px' }}>
                    <div className="progress-bar progress-bar-striped" role="progressbar"
                        style={{ width: `${parseInt(percentage)}%`, backgroundColor: color }}>
                        {parseInt(percentage)}%
                    </div>
                </div>
                <h2 className="card-title pricing-card-title">
                    {rate.toFixed(2)} <span>{unit}</span>
                    <small className="text-muted fw-light">
                        /{secondary_unit}
                    </small>
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
                <Link to={`/bar/${bar_name}`} type="button" className="w-100 btn btn-lg btn-outline-success">
                    Details
                </Link>
                <a onClick={onClose} type="button" className="btn p-0 position-absolute top-0 right-4">
                    <span>×</span>
                </a>
            </div>
        </div>
    </div>
);