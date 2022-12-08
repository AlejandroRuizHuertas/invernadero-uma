
export const loginUser = async (credentials) => {
    try {
        console.log(credentials)
        const response = await fetch(process.env.REACT_APP_HTTPAPI + '/admin/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        });
        return response.json()
    }
    catch(error){
        console.log(error)
    }
}
