import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

function HomeButton() {
    const navigate = useNavigate();
    return(
        <button onClick={ () => navigate('/')}>
            <span class="iconify-home" />
        </button>
    )
}

function Location() {
    const [location, setLocation] = useState('');
    let locations = [];
    locations.push(<option value={''}>{''}</option>)
    locations.push(<option value={'the united states'}>{'the united states'}</option>)
    locations.push(<option value={'canada'}>{'canada'}</option>)
    locations.push(<option value={'australia'}>{'australia'}</option>)
    locations.push(<option value={'india'}>{'india'}</option>)
    
    const handleChange = event => {
        event.preventDefault()
        setLocation(event.target.value)
    };
    
    return(
        <div>
            <form>
                <label>
                    Location
                    <select value={location} onChange={handleChange}>
                        { locations }
                    </select>
                </label>
            </form>
        </div>
    );
}

function Month() {
    const [month, setMonth] = useState('');
    let months = [];
    months.push(<option value={''}>{''}</option>)
    months.push(<option value={'1'}>{'January'}</option>)
    months.push(<option value={'2'}>{'February'}</option>)
    months.push(<option value={'3'}>{'March'}</option>)
    months.push(<option value={'4'}>{'April'}</option>)
    months.push(<option value={'5'}>{'May'}</option>)
    months.push(<option value={'6'}>{'June'}</option>)
    months.push(<option value={'7'}>{'July'}</option>)
    months.push(<option value={'8'}>{'August'}</option>)
    months.push(<option value={'9'}>{'September'}</option>)
    months.push(<option value={'10'}>{'October'}</option>)
    months.push(<option value={'11'}>{'November'}</option>)
    months.push(<option value={'12'}>{'December'}</option>)

    
    const handleChange = event => {
        setMonth(event.target.value);
        
    };
    return(
        <div>
            <form>
                <label>
                    Month of Review
                    <select value={month} onChange={handleChange}>
                        { months }
                    </select>
                </label>
            </form>
        </div>
    );
}




function Filters() {
    return(
        <div>
            <h1>Filters</h1>
            <Location />
            <Month />
        </div>
    );
}

function TopBar() {
    return(
        <div class="App-topbar">
            <HomeButton />
            <h1>ReviewZ</h1>
        </div>
    );
}

function Graph() {
    const onClick = event => (
        fetch('/get_image')
          .then(function(data){
          document.getElementById('progress').textContent = "Loading";
          return data.blob();
        })
        .then(blob => {
          var img = URL.createObjectURL(blob);
          // const dd = imagesrc
          // $('#progress').text("");
          // $('img').attr('src', dd);
          document.getElementById('progress').textContent = "Loaded"
          document.getElementById('test').setAttribute('src', img);
        })
      );

    return(
        <div>
            <button id="btn" onClick={onClick} >Get Image</button>
            <img src="" id="test" alt=""  width="500px" />
            <div id="progress"></div>
            <GraphOption />
        </div>
    )
}

function GraphOption() {
    const [graphOption, setGraphOption] = useState('Histogram');
    let graphOptions = [];
    graphOptions.push(<option value={'Histogram'}>{'Histogram'}</option>)
    graphOptions.push(<option value={'Heat Map'}>{'Heat Map'}</option>)

    const handleChange = event => {
        setGraphOption(event.target.value);
    };
    return(
        <div>
            <form>
                <label>
                    Graph Option
                    <select value={graphOption} onChange={handleChange}>
                        { graphOptions }
                    </select>
                </label>
            </form>
        </div>
    );
}

export default function Analyzer() {
    return (
        <header class="App-analyzer">
            <TopBar />
            <Filters />
            <Graph />
        </header> 
    );
}