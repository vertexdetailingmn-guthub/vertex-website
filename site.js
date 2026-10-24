(function(){
  /* vehicle-size price toggle */
  var btns=document.querySelectorAll('.toggle button');
  var prices=document.querySelectorAll('[data-prices]');
  function setSize(i){
    btns.forEach(function(b){b.setAttribute('aria-pressed',String(Number(b.dataset.size)===i));});
    prices.forEach(function(p){p.textContent='$'+p.dataset.prices.split(',')[i];});
    try{localStorage.setItem('vtx-size',String(i));}catch(e){}
  }
  btns.forEach(function(b){b.addEventListener('click',function(){setSize(Number(b.dataset.size));});});
  var saved=null; try{saved=localStorage.getItem('vtx-size');}catch(e){}
  if(saved!==null && btns.length) setSize(Number(saved));

  /* before/after sliders */
  document.querySelectorAll('.cmp input').forEach(function(r){
    r.addEventListener('input',function(){r.parentElement.style.setProperty('--x',r.value+'%');});
  });

  /* quick quote -> /api/lead (Cloudflare Function) -> OrbisX Lead API */
  var qf=document.getElementById('quickform');
  if(qf){
    qf.addEventListener('submit',function(e){
      e.preventDefault();
      if(!qf.checkValidity()){qf.reportValidity();return;}
      var fd=new FormData(qf);
      var data={contact:fd.get('contact'),phone:fd.get('phone'),city:fd.get('city'),interest:fd.get('interest'),
        notes:'Quick quote request from website. Vehicle: '+fd.get('vehicle')+'. City: '+fd.get('city')+'.'};
      var v=(fd.get('vehicle')||'').match(/^(\d{4})\s+(\S+)\s+(.+)$/);
      if(v){data.auto_year=v[1];data.auto_make=v[2];data.auto_model=v[3];}
      var btn=document.getElementById('q-submit'); btn.disabled=true;
      fetch('/api/lead',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(data)})
        .catch(function(){})
        .then(function(){document.getElementById('q-done').hidden=false;});
    });
  }
})();
