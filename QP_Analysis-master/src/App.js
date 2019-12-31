import React, { useState } from 'react';
import { Row, Col } from 'antd';
import axios from 'axios';
import PieChart from 'react-minimal-pie-chart';
import './App.css';

/**
 *  Change the proxy URL in package.json to your backend route
 *  Look for console.log and change the variable in setResult method
 *  
 */


function App() {

  
  const [image, setImage] = useState({preview: '', raw: ''});
  const [result, setResult] = useState({res:''});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setImage({
        preview: URL.createObjectURL(e.target.files[0]),
      raw: e.target.files[0],
      
        
    });
  }

  const handleUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("image", image.raw);
    const config = { headers: { 'content-type': 'multipart/form-data' } };
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:3000/', formData, config);
      
      setResult({
        res: res.data.result
      }); // Check the console log and change it appropriately 
     console.log(res.data);
      setLoading(false);

    } catch(err) {
      console.log("Catched Error" , err);
    }

  }
  // const jsx = ''; 
  // if(result != null) {
  //   Object.keys(result.res).map((data, key) => {
  //     return (
  //       <Row key={key}>
  //         <Col span="4">
  //           <h4>{data}</h4>
  //         </Col>
  //         <Col span="4">
  //           <h4>{result[data]}%</h4>
  //         </Col>
  //       </Row>
  //     )
  //   })
  // }
  return (
    <div>
      <h1 className = "title">Question Paper Analysis</h1>
      <br/>
      <Row>
        <Col span = {12}>
          <h2>Upload your Question paper</h2>
          <form onSubmit={handleUpload}>
          {
              image.preview ? 
              <img src={ image.preview } width="85%" height="100%" alt="preview" /> 
              : <input type="file" name="image" onChange = {handleChange} />                
          }
          <input type="submit" />
        </form>
          
        </Col>

        <Col span = {12}>
          {loading && <h2>Processing....</h2>}
          
        </Col>
      </Row>
      {result != null && <PieChart
        data={[
          { title: 'One', value: 10, color: '#E38627' },
          { title: 'Two', value: 15, color: '#C13C37' },
          { title: 'Three', value: 20, color: '#6A2135' },
        ]}
      />}
      
            
    </div>
  );
}

export default App;
