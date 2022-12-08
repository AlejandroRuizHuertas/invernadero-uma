
export const getData = async (servicio) => {
    try {
        const token = localStorage.getItem('token')
        const response = await fetch(process.env.REACT_APP_HTTPAPI+servicio, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization':token
                
            }
        });        
        return response.json()
    }
    catch(error){
        console.log(error)
    }
}

export const postData = async (servicio, payload) => {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(process.env.REACT_APP_HTTPAPI+servicio, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization':token
                
            },
            body: payload
        });        
        return response.json()
    }
    catch(error){
        console.log(error)
    }
}
