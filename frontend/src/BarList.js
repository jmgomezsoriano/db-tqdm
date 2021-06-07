import React, { useState, useEffect } from 'react';
import './App.css';
import Bar from './Bar';

const API_URL_BARS = '/api/tqdm';

export default () => {
    const [bars, setBars] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(false);
    
    useEffect(() => {
        const intervalId = setInterval(() => {
            //assign interval to a variable to clear it.
            setError(false);
            setLoading(true);
            fetch(API_URL_BARS)
                .then((res) => res.json())
                .then((data) => {
                    if (data.bars) {
                        setBars(data.bars);
                    } else {
                        console.log("No 'bars' in the response body.");
                        setError(true);
                    }
                    setLoading(false);
                })
                .catch(function (error) {
                    console.log(error);
                    setError(true);
                    setLoading(false);
                });
        }, 5000);
        return () => clearInterval(intervalId); //This is important
    }, []);

    const removeBar = (bar_name) => setBars(bars.filter((bar) => bar.bar_name !== bar_name));

    return (
        <div className="App row row-cols-1 row-cols-md-2 row-cols-lg-3 mb-3 text-center" >
            {bars.map((bar) => (
                <Bar id={bar.bar_name} onClose={() => removeBar(bar.bar_name)} {...bar} />
            ))}
        </div>
    );
};
