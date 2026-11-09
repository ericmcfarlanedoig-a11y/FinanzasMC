const {chromium}=require('playwright');
(async()=>{
  const [,,html,out,fps,only]=process.argv;
  const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
  await pg.goto('file://'+html+'?capture');await pg.evaluate(()=>document.fonts.ready);
  const dur=await pg.evaluate(()=>window.DUR);const F=Number(fps);
  const times= only? only.split(',').map(Number) : [...Array(Math.round(dur*F)).keys()].map(i=>i/F);
  for(let i=0;i<times.length;i++){await pg.evaluate(t=>render(t),times[i]);
    await pg.screenshot({path:`${out}/f${String(i).padStart(5,'0')}.png`});}
  await b.close();
})();
