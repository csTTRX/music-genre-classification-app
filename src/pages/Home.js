import React from 'react'
import { useState } from 'react'
import axios from 'axios'
import Loading from '../conponents/Loading';

const Home = () => {
    const [file, setFile] = useState()
    const [file_name, setFile_name] = useState()
    const [result, setResult] = useState()
    const [uploaded, setUploaded] = useState(null)
    const [loading, setLoading] = useState(false)

    const formData = new FormData();
    formData.append('file_name', file);

    const HandleSubmit = (e) =>{
        e.preventDefault()
        setLoading(true)
        axios({
            url:'http://127.0.0.1:8000/api/',
            method:'post',
            mode : 'cors',
            headers : {
                //"Content-Type":"multipart/form-data",
                'X-CSRFToken': 'csrftoken'
            },
            data:formData,
            onUploadProgress: (data) =>{
                setUploaded(Math.round((data.loaded / data.total)*100))
                console.log(data.loaded, data.total)
            }
        }).then(res =>{
            setResult(res.data)
            setLoading(false)
        })
    }
    const handleChange = (e)=>{
        setFile_name(e.target.files[0].name)
        setFile(e.target.files[0])
    }
  return (
    <div className='home'>
        <div className='header'>
            <h1 className='logo'>Music<span>Genre</span></h1>
                <p> Recognize the genres of the music you listen to. Just upload a music audio file and our app will classify it into one of 10 music genres which are:
                <span>Blues</span> <span>Classical</span> <span>Country</span> <span>Disco</span> <span>Hiphop</span> <span>Jazz</span> <span>Metal</span> <span>Pop</span> <span>Reggae</span> <span>Rock</span></p>
                <p className='accept-file'>Accepted <span>mp3</span> <span>ma4</span> and <span>wav</span> audio file.</p>
        
        </div>
        <div className='form-box'>
            {loading ? (<Loading />): ( result && <div className = 'result'> <p>The Genre fo this music is <span>{result}</span></p></div>)}
            <form action="" onSubmit={HandleSubmit} encType = 'multipart/form-data'>
                <label htmlFor="updload">
                    <p> Select a file</p>
                </label>
                <input type= 'file' id ='updload' name = 'file_name' accept = 'audio/*' onChange={handleChange} hidden required></input>
                <button type='submit'> Submit</button>
            </form>

            {file && (<div className = 'selected-file'>{file_name}</div>)}

            {uploaded && <div className = 'progress'>
                <div className='progress-bar' 
                role='progressbar'
                aria-valuenow={uploaded}
                aria-valuemin = '0'
                aria-valuemax='100'
                style={{width: `${uploaded}%`}}
                >
                    {`${uploaded}%`}
                </div>
            </div>}
        </div>

        <div className='footer'>
            <p> 
              All uploaded data will be <span>immediately</span> delete after
            </p>
            <p>Copyright © 2022 by csttrx.</p>
        </div>
    </div>
  )
}

export default Home
