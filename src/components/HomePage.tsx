import React from 'react';
import spotifyBg from '../assets/spotifybg.jpg';
import monsterCartoon from '../assets/monstercartoon.png';
import spotifyLogo from '../assets/Spotifylogo.png';

const YourComponent: React.FC = () => {
  const handleSpotifyLogin = () => {
    window.location.href = '/login';
  };

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      position: 'relative',
      overflow: 'hidden',
    }}>
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundImage: 'linear-gradient(rgba(174, 248, 174, 1), rgba(255, 255, 255, 1))',
        opacity: 1,
        zIndex: 0,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
      }}></div>
      
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundImage: `url(${spotifyBg})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        opacity: 0.2,
        zIndex: 1,
      }}></div>

      <div style={{
        width: 666,
        height: 693,
        right: '17%',
        top: '45%',
        transform: 'translateY(-50%)',
        position: 'absolute',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 2,
        backgroundColor: 'rgba(30, 215, 96, 0.5)',
        boxShadow: '15px 18px 11.1px 5px rgba(0, 0, 0, 0.80)',
        borderRadius: '50%',
        border: '3px solid black',
        padding: 20,
        boxSizing: 'border-box',
      }}>
        <div style={{
          position: 'relative',
          width: 505,
          height: 502,
        }}>
          <img style={{
            width: 254,
            height: 315,
            position: 'absolute',
            left: 0,
            top: 170,
            filter: 'brightness(20%)', 
          }} src={monsterCartoon} alt="Monster Cartoon" />
          <img style={{
            width: 253,
            height: 315,
            position: 'absolute',
            left: 252,
            top: 170,
            filter: 'brightness(20%)',
          }} src={monsterCartoon} alt="Monster Cartoon" />
          <img style={{
            width: 406,
            height: 502,
            position: 'absolute',
            left: 50,
            top: 0,
          }} src={monsterCartoon} alt="Monster Cartoon" />
        </div>
      </div>

      <div style={{
        left: 86,
        top: 38,
        position: 'absolute',
        justifyContent: 'center',
        alignItems: 'flex-start',
        gap: 3,
        display: 'inline-flex',
        zIndex: 3,
      }}>
        <div style={{
          color: 'black',
          fontSize: 30,
          fontFamily: 'Montserrat',
          fontWeight: 700,
          wordWrap: 'break-word',
        }}>YourMusicCharacter</div>
        <img style={{
          width: 38,
          height: 40,
        }} src={spotifyLogo} alt="Spotify Logo" />
      </div>

      <div style={{
        width: 618,
        height: 84,
        left: 262,
        top: 727,
        position: 'absolute',
        zIndex: 3,
      }}>
        <div style={{
          width: 618,
          height: 84,
          left: 250,
          top: 100,
          position: 'absolute',
          background: 'black',
          boxShadow: '0px 4px 4px rgba(0, 0, 0, 0.25)',
          borderRadius: 15,
          border: '2px solid black',
        }}></div>
        <div style={{
          width: 517,
          height: 48,
          left: 300,
          top: 112,
          position: 'absolute',
          textAlign: 'center',
          zIndex: 4,
        }}>
          <span style={{
            color: 'white',
            fontSize: 35,
            fontFamily: 'Montserrat',
            fontWeight: 700,
            wordWrap: 'break-word',
          }}> Link Your </span>
          <span style={{
            color: '#1ED760',
            fontSize: 35,
            fontFamily: 'Montserrat',
            fontWeight: 700,
            wordWrap: 'break-word',
          }}>Spotify</span>
          <span style={{
            color: 'white',
            fontSize: 35,
            fontFamily: 'Montserrat',
            fontWeight: 700,
            wordWrap: 'break-word',
          }}> Account!</span>
          <span style={{
            color: 'white',
            fontSize: 40,
            fontFamily: 'Montserrat',
            fontWeight: 700,
            wordWrap: 'break-word',
          }}> </span>
        </div>
      </div>

      <div style={{
        left: 424,
        top: 282,
        position: 'absolute',
        justifyContent: 'center',
        alignItems: 'center',
        display: 'inline-flex',
        zIndex: 3,
      }}>
        <div style={{
          color: 'black',
          fontSize: 140,
          fontFamily: 'Montserrat',
          fontWeight: 800,
          wordWrap: 'break-word',
        }}>Welcome!</div>
      </div>

      <div style={{
        left: 512,
        top: 465,
        position: 'absolute',
        justifyContent: 'center',
        alignItems: 'center',
        display: 'inline-flex',
        zIndex: 3,
      }}>
        <div style={{
          color: 'black',
          fontSize: 40,
          fontFamily: 'Montserrat',
          fontWeight: 700,
          wordWrap: 'break-word',
        }}>To A Spotify Personality Test</div>
      </div>

      <div style={{
        width: 725,
        height: 111,
        left: 452,
        top: 555,
        position: 'absolute',
        justifyContent: 'center',
        alignItems: 'center',
        display: 'inline-flex',
        zIndex: 3,
      }}>
        <div style={{
          width: 725,
          color: 'black',
          fontSize: 30,
          fontFamily: 'Montserrat',
          fontWeight: 500,
          wordWrap: 'break-word',
        }}>Sign in to Your Spotify Account Then Get <br />Personality-Based Cartoon Characters From <br />Your Top 5 Most Listened to Spotify Songs!</div>
      </div>

      <div style={{
        position: 'absolute',
        bottom: 20,
        width: '100%',
        display: 'flex',
        justifyContent: 'center',
        zIndex: 3,
      }}>
        <button
          style={{
            padding: '15px 30px',
            fontSize: '20px',
            fontWeight: 'bold',
            color: 'white',
            backgroundColor: '#1ED760',
            border: 'none',
            borderRadius: '25px',
            cursor: 'pointer',
          }}
          onClick={handleSpotifyLogin}
        >
          Link Your Spotify Account!
        </button>
      </div>

      <div style={{
        position: 'absolute',
        bottom: 0,
        width: '100%',
        height: '80px',
        background: 'rgba(0, 0, 0, 0.20)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        color: 'black',
        fontFamily: 'Montserrat',
        fontWeight: 700,
        fontSize: 24,
      }}>
        A Tech Cadet Project
      </div>
    </div>
  );
};

export default YourComponent;
