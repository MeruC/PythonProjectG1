document.addEventListener('DOMContentLoaded', ()=>{
    const selectDrop = document.querySelector('#company_country');
  
    fetch('https://restcountries.com/v3.1/all').then(res=>res.json()).then(data=>{
        data.forEach(country=>{
            const option = document.createElement('option');
            option.value = country.name.common;
            option.text = country.name.common;
            selectDrop.appendChild(option);
        })
    })
    
})