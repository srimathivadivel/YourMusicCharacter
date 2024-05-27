import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const CharacterPage = () => {
    const { songId } = useParams();
    const [meme, setCharacter] = useState('');

    useEffect(() => {
        const fetchCharacter = async () => {
            try {
                const response = await axios.get(`/get-character/${songId}`);
                setCharacter(response.data.characterUrl);
            } catch (error) {
                console.error('Error fetching character:', error);
            }
        };

        fetchCharacter();
    }, [songId]);

    return (
        <div className="character-page">
            <h1>Here's a character for your song!</h1>
            <img src={character} alt="Character" />
        </div>
    );
};

export default CharacterPage;
