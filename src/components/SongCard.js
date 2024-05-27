import React from 'react';
import { useHistory } from 'react-router-dom';

const SongCard = ({ song }) => {
    const history = useHistory();

    const handleClick = () => {
        history.push(`/character/${song.id}`);
    };

    return (
        <div className="song-card" onClick={handleClick}>
            <h2>{song.name}</h2>
            <p>{song.artist}</p>
        </div>
    );
};

export default SongCard;
