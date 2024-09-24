const getAuthTokenFromCookie = () => {
    const cookies = document.cookie;
    const cookieArr = cookies.split(';').map(cookie => cookie.trim().split('='));
    const tokenCookie = cookieArr.find(cookie => cookie[0] === 'bearerToken');
  
    return tokenCookie ? tokenCookie[1] : null;
  };
  
  export { getAuthTokenFromCookie} ;
  