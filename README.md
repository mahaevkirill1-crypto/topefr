<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Car Roulette</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Russo+One&family=Sora:wght@400;600;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0}html,body{height:100%}
body{background:radial-gradient(90% 55% at 50% 38%,#4a2391,#170b34 62%,#07040f);color:#fff;font:14px Sora,sans-serif;display:flex;flex-direction:column;overflow:hidden;padding-top:env(safe-area-inset-top,0)}
body:before{content:"";position:fixed;left:50%;top:38%;width:900px;height:900px;margin:-450px 0 0 -450px;background:repeating-conic-gradient(rgba(255,200,80,.12) 0 9deg,transparent 9deg 18deg);-webkit-mask:radial-gradient(circle,#000,transparent 62%);mask:radial-gradient(circle,#000,transparent 62%);pointer-events:none}
.ru{font-family:"Russo One",sans-serif;font-weight:400}
#top{position:relative;display:flex;gap:8px;padding:12px 14px 0}
.pill{display:flex;align-items:center;gap:8px;background:#0b0618bb;border:1px solid #ffffff2a;border-radius:22px;padding:5px 12px 5px 5px;font:600 15px Sora}
.coin{width:26px;height:26px;border-radius:50%;background:linear-gradient(#ffe08a,#e8a317);color:#5a3a00;display:flex;align-items:center;justify-content:center;font-size:14px}
#main{position:relative;flex:1;overflow-y:auto;padding:10px 16px;display:flex;flex-direction:column;align-items:center}
.b3{border:0;border-radius:20px;font:400 19px "Russo One",sans-serif;letter-spacing:.05em;color:#fff;width:100%;height:58px;margin-top:14px}
.b3:disabled{opacity:.45}.gold{background:linear-gradient(#ffd76a,#f5a300);box-shadow:0 6px 0 #a35f00,0 12px 26px #f5a30066;color:#3a2200}
.vio{background:linear-gradient(#9d6bff,#6a35e6);box-shadow:0 6px 0 #3b1a9c;height:50px;font-size:15px}
.sm{width:auto;height:38px;font-size:13px;padding:0 14px;margin:0;box-shadow:0 4px 0 #a35f00}.gr{background:#4b4470;box-shadow:0 4px 0 #2a2545;color:#fff}
.nav{position:relative;display:flex;justify-content:space-around;background:#0b0618;border-top:1px solid #ffffff18;padding:8px 0 calc(10px + env(safe-area-inset-bottom,0))}
.ni{display:flex;flex-direction:column;align-items:center;font:600 11px Sora;color:#8a84a8;background:none;border:0}.ni i{font-style:normal;font-size:20px}.on{color:#ffd76a}.on i{filter:drop-shadow(0 0 8px #f5a300)}
#win{width:100%;max-width:350px;height:230px;border-radius:26px;border:3px solid #ffd76a;background:#0b0618d9;box-shadow:0 0 44px var(--rc,#a855f755),inset 0 0 34px #000;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;text-align:center;padding:8px}
#em{font-size:92px;line-height:1}#nm{font-size:20px}
.card{width:100%;border-radius:18px;border:2px solid var(--c,#ffffff2a);background:linear-gradient(#1d1040,#110a28);box-shadow:0 0 18px var(--c,transparent);padding:12px;margin-bottom:10px}
.row{display:flex;align-items:center;gap:8px}.bar{height:8px;background:#ffffff22;border-radius:4px;margin:8px 0 4px;overflow:hidden}.bar i{display:block;height:100%;background:linear-gradient(90deg,#34d399,#10b981)}
#wh{width:290px;height:290px;border-radius:50%;border:8px solid #ffd76a;box-shadow:0 0 44px #f5a30088,inset 0 0 30px #0008;position:relative}
#wh span{position:absolute;left:50%;top:50%;width:70px;margin:-12px 0 0 -35px;text-align:center;font:400 17px "Russo One";text-shadow:0 2px 4px #000}
#md{position:fixed;inset:0;background:#000a;display:none;align-items:center;justify-content:center;padding:20px;z-index:9}
.cf{position:fixed;top:-14px;width:8px;height:12px;z-index:30;animation:fl 2.6s linear forwards}@keyframes fl{to{transform:translateY(110vh) rotate(720deg)}}
</style></head><body>
<div id="top"><div class="pill"><span class="coin">★</span><span id="s"></span></div><div class="pill"><span class="coin" style="background:linear-gradient(#b8f5c8,#2fb457);color:#073d1a">₽</span><span id="m"></span></div></div>
<div id="main"></div>
<div class="nav" id="nav"><button class="ni" onclick="go(0)"><i>◉</i>Рулетка</button><button class="ni" onclick="go(1)"><i>▤</i>Гараж</button><button class="ni" onclick="go(2)"><i>♛</i>Топ</button><button class="ni" onclick="go(3)"><i>✦</i>Бонусы</button><button class="ni" onclick="go(4)"><i>◆</i>Магазин</button></div>
<div id="md"></div>
<script>
const BOT='ИМЯ_БОТА',$=id=>document.getElementById(id),sleep=ms=>new Promise(r=>setTimeout(r,ms)),rnd=a=>a[Math.random()*a.length|0],fmt=n=>Math.round(n).toLocaleString('ru-RU');
const tg=window.Telegram&&Telegram.WebApp;if(tg){tg.ready();tg.expand()}
const UID=tg&&tg.initDataUnsafe&&tg.initDataUnsafe.user?tg.initDataUnsafe.user.id:'demo';
const R=[{n:'ХЛАМ',c:'#9aa0a8',f:60,p:35,s:.8},{n:'РЕДКИЙ',c:'#3b82f6',f:25,p:28,s:1.2},{n:'ЭПИЧЕСКИЙ',c:'#a855f7',f:10,p:18,s:2},{n:'МИФИЧЕСКИЙ',c:'#ef4444',f:4,p:12,s:3},{n:'ЛЕГЕНДАРНЫЙ',c:'#f5b301',f:1,p:7,s:4.5}],E=['🛻','🚗','🚙','🏎️','🏎️'];
// цена в тысячах ₽, строго внутри диапазона редкости (хлам до 500 тыс, редкие 0.5–2 млн, эпик 2–10 млн, миф 10–50 млн, лега 50 млн–1 млрд)
const C=[[['ВАЗ 2109',90],['Daewoo Matiz',180],['Lada Granta',420],['ВАЗ 2107',70],['Chevrolet Lanos',250],['Lada Niva',480],['ЗАЗ Сенс',110],['Москвич 2141',60]],
[['Kia Rio',1100],['Hyundai Solaris',1200],['Skoda Octavia',1800],['Volkswagen Polo',1400],['Renault Logan',700],['Renault Duster',1900],['Ford Focus',1000],['Nissan Almera',900]],
[['Toyota Camry',3200],['BMW 3',4500],['Audi A4',3900],['Mercedes E-Class',7500],['Porsche Macan',9000],['Lexus RX',6800],['Volvo XC90',5900],['BMW M5',9500]],
[['Lamborghini Urus',28e3],['Ferrari 488',24e3],['Bentley Continental GT',21e3],['Mercedes G63 AMG',19e3],['Rolls-Royce Ghost',38e3],['Porsche 911 Turbo S',17e3],['Aston Martin DB11',15e3],['McLaren 570S',14e3]],
[['Rolls-Royce Cullinan',62e3],['Pagani Huayra',18e4],['Koenigsegg Jesko',25e4],['Bugatti Chiron',32e4],['Bugatti La Voiture Noire',9e5],['Lamborghini Veneno',45e4],['Ferrari LaFerrari',19e4],['McLaren P1',15e4]]];
const Q=[[0,'Прокрути рулетку 20 раз','spins',20,1],[0,'Выбей 5 машин «Редкие» или выше','rare',5,2],[0,'Продай 3 машины','sold',3,2],[0,'Открой гараж 3 раза','gar',3,1],[0,'Открой профиль игрока из топа','prof',1,1],[0,'Поделись выпавшей машиной','share',1,2],[0,'Забери бонусное колесо','wheel',1,2],
[1,'Прокрути рулетку 100 раз','spins',100,5],[1,'Выбей 3 эпические машины или выше','epic',3,5],[1,'Продай 5 машин','sold',5,3],[1,'Сделай 1 платную крутку','paid',1,3],[1,'Продай машин на 5 000 000 ₽','soldsum',5e6,5],[1,'Прокрути рулетку 50 раз','spins',50,4],
[2,'Выбей легендарную машину','leg',1,10],[2,'Выбей мифическую машину или выше','myth',1,7],[2,'Прокрути рулетку 300 раз','spins',300,10],[2,'Сделай 3 платные крутки','paid',3,8],[2,'Выбей машину дороже 100 000 000 ₽','big',1,15]];
const B=[['Макс_Drive',[[4,4],[4,3],[3,0]]],['Анна',[[4,1],[3,2],[2,4]]],['Ильдар',[[3,4],[3,1],[2,0]]],['Сергей',[[2,3],[2,1],[1,2]]],['Kolya99',[[1,0],[0,2]]]];
let S={s:40,m:0,g:[],w:0,q:{day:'',prog:{},claimed:{},ids:[]}},busy=0,T=0,cur=0,last=null;
try{Object.assign(S,JSON.parse(localStorage.getItem('cr2')||'{}'))}catch(e){}
const save=()=>{try{localStorage.setItem('cr2',JSON.stringify(S))}catch(e){}},bal=()=>{$('s').textContent=S.s;$('m').textContent=fmt(S.m)};
const tr=(k,n=1)=>{S.q.prog[k]=(S.q.prog[k]||0)+n;save()};
const today=()=>new Date(Date.now()+108e5).toISOString().slice(0,10);
function seed(s){let h=0;for(const c of s)h=Math.imul(31,h)+c.charCodeAt(0)|0;return()=>{h=h+0x6D2B79F5|0;let t=Math.imul(h^h>>>15,1|h);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function dayQ(day,prev){const r=seed(day),o=[];[[0,2],[1,2],[2,1]].forEach(([d,n])=>{const a=Q.map((q,i)=>i).filter(i=>Q[i][0]==d&&!prev.includes(i));while(n--)o.push(a.splice(r()*a.length|0,1)[0])});return o}
function newDay(){const p=S.q.ids||[];S.q={day:today(),prog:{},claimed:{},ids:dayQ(today(),p)};save()}
const md=h=>{$('md').innerHTML='<div class="card" style="--c:#ffd76a;max-width:330px;text-align:center">'+h+'<button class="b3 gold" onclick="cl()">OK</button></div>';$('md').style.display='flex'},cl=()=>{$('md').style.display='none'};
function ask(h,fn){window._f=fn;$('md').innerHTML='<div class="card" style="--c:#ffd76a;max-width:330px;text-align:center">'+h+'<button class="b3 gold" onclick="cl();_f()">Да</button><button class="b3 vio" onclick="cl()">Отмена</button></div>';$('md').style.display='flex'}
function confetti(){for(let i=0;i<40;i++){const d=document.createElement('div');d.className='cf';d.style.left=Math.random()*100+'vw';d.style.background=rnd(['#f5b301','#ef4444','#3b82f6','#10b981']);d.style.animationDelay=Math.random()*.6+'s';document.body.append(d);setTimeout(()=>d.remove(),3600)}}
function share(t){tr('share');const u='https://t.me/share/url?url='+encodeURIComponent('https://t.me/'+BOT)+'&text='+encodeURIComponent(t);tg&&tg.openTelegramLink?tg.openTelegramLink(u):window.open(u,'_blank')}
function add(ri,c){const o={u:Math.random().toString(36).slice(2),r:ri,n:c[0],p:c[1]*1e3};S.g.push(o);if(ri>=1)tr('rare');if(ri>=2)tr('epic');if(ri>=3)tr('myth');if(ri==4)tr('leg');if(o.p>1e8)tr('big');save();return o}
function sell(u){const i=S.g.findIndex(c=>c.u==u);if(i<0)return;const c=S.g.splice(i,1)[0];S.m+=c.p;tr('sold');tr('soldsum',c.p);bal();save()}
function go(t){if(busy)return;T=t;[...$('nav').children].forEach((b,i)=>b.classList.toggle('on',i==t));if(t==1)tr('gar');[vr,vg,vt,vb,vm][t]()}
// ---- Рулетка ----
function vr(){$('main').innerHTML=`<div class="ru" id="rt" style="font-size:26px;margin-top:4px">КРУТИ!</div><div id="pr" class="ru" style="font-size:34px;color:#ffe08a;height:46px;opacity:0;transition:opacity .6s">&nbsp;</div><div id="win"><div id="em">❓</div><div id="nm" class="ru">???</div></div><div id="ac" style="margin-top:12px"></div><button class="b3 gold" id="b1" onclick="spin(0)">КРУТИТЬ БЕСПЛАТНО</button><button class="b3 vio" id="b2" onclick="spin(1)">КРУТИТЬ ЗА 20 ★ · ШАНС ВЫШЕ</button><div style="font-size:11px;color:#b9b0e0;margin-top:12px;text-align:center">Шансы (беспл./платно): ${R.map(r=>r.n.slice(0,4)+' '+r.f+'/'+r.p+'%').join(' · ')}</div>`}
function show(k,n){$('win').style.setProperty('--rc',R[k].c);$('em').textContent=E[k];$('nm').textContent=n}
const roll=p=>{let x=Math.random()*100,i=0;for(;i<4;i++){x-=R[i][p?'p':'f'];if(x<0)break}return i};
const count=(el,to,ms,col,gl)=>new Promise(r=>{const t0=performance.now();el.style.color=gl?col:'#ffe08a';(function f(n){const p=Math.min((n-t0)/ms,1);el.textContent=fmt(to*(1-Math.pow(1-p,3)))+' ₽';if(p<1)requestAnimationFrame(f);else{if(gl)el.animate([{transform:'scale(1.3)'},{transform:'scale(1)'}],350);r()}})(t0)});
async function spin(p){if(busy)return;if(p){if(S.s<20)return md('Не хватает ★ для платной крутки.');S.s-=20;tr('paid')}
 busy=1;$('b1').disabled=$('b2').disabled=true;$('ac').innerHTML='';bal();
 const ri=roll(p),car=rnd(C[ri]),pr=$('pr');pr.style.opacity=0;pr.textContent='\u00a0';$('rt').textContent='КРУТИМ...';$('rt').style.color='#fff';
 const t0=performance.now();
 while(performance.now()-t0<3500){const k=Math.random()*5|0;show(k,rnd(C[k])[0]);await sleep(45+(performance.now()-t0)/3500*300)}
 show(ri,car[0]);$('rt').textContent=R[ri].n;$('rt').style.color=R[ri].c;
 if(ri==4){await sleep(500);confetti()}
 pr.style.opacity=1;await count(pr,car[1]*1e3,R[ri].s*1000,R[ri].c,ri>=3);
 last=add(ri,car);tr('spins');bal();
 $('ac').innerHTML=`<div class="row"><button class="b3 gold sm" onclick="sellLast()">ПРОДАТЬ</button><button class="b3 gr sm" onclick="share('Мне выпала ${car[0]} за ${fmt(car[1]*1e3)} ₽ в Car Roulette!')">ПОДЕЛИТЬСЯ</button></div>`;
 $('b1').disabled=$('b2').disabled=false;busy=0}
function sellLast(){if(last){sell(last.u);last=null;$('ac').innerHTML=''}}
// ---- Гараж ----
function vg(){const tot=S.g.reduce((a,c)=>a+c.p,0);$('main').innerHTML=`<div class="ru" style="font-size:26px;align-self:flex-start">ГАРАЖ</div><div style="align-self:flex-start;color:#b9b0e0;margin:4px 0 12px">${S.g.length} машин · стоимость <b class="ru" style="color:#ffe08a">${fmt(tot)} ₽</b></div>`+(S.g.length?S.g.slice().reverse().map(c=>`<div class="card" style="--c:${R[c.r].c}"><div class="row"><span style="font-size:42px">${E[c.r]}</span><div style="flex:1"><b>${c.n}</b><br><small class="ru" style="color:${R[c.r].c}">${R[c.r].n}</small> <small class="ru" style="color:#ffe08a">${fmt(c.p)} ₽</small></div></div><div class="row" style="margin-top:10px"><button class="b3 gold sm" onclick="ask('Продать ${c.n} за ${fmt(c.p)} ₽?',()=>{sell(\\'${c.u}\\');vg()})">ПРОДАТЬ</button><button class="b3 gr sm" onclick="share('Моя ${c.n} в Car Roulette!')">ПОДЕЛИТЬСЯ</button></div></div>`).join(''):'<p style="color:#b9b0e0;margin-top:60px">Гараж пуст. Крути рулетку!</p>')}
// ---- Топ ----
function vt(){const e=B.map(([n,l])=>({n,l:l.map(([r,i])=>({r,n:C[r][i][0],p:C[r][i][1]*1e3}))}));e.push({n:'Вы',l:S.g});e.forEach(x=>x.t=x.l.reduce((a,c)=>a+c.p,0));window._e=e.sort((a,b)=>b.t-a.t);
 $('main').innerHTML='<div class="ru" style="font-size:26px;align-self:flex-start">ТОП ИГРОКОВ</div><p style="color:#b9b0e0;font-size:12px;margin:4px 0 12px;align-self:flex-start">Демо-рейтинг. Общий топ работает с сервером.</p>'+_e.map((x,i)=>`<div class="card row" onclick="prof(${i})"><b class="ru" style="flex:1">${i+1}. ${x.n}</b><span class="ru" style="color:#ffe08a">${fmt(x.t)} ₽</span></div>`).join('')}
function prof(i){tr('prof');const x=_e[i];md(`<b class="ru">${x.n}</b><br><small>${fmt(x.t)} ₽ · машин: ${x.l.length}</small><div style="text-align:left;max-height:45vh;overflow:auto;margin-top:8px">${x.l.map(c=>`<div style="border-left:5px solid ${R[c.r].c};padding:3px 8px;margin:4px 0"><small>${E[c.r]} ${c.n} — ${fmt(c.p)} ₽</small></div>`).join('')}</div>`)}
// ---- Бонусы ----
const W=['★5','МИФ','★10','ЛЕГ','★50'],WC=['#3b82f6','#ef4444','#8b5cf6','#f5b301','#10b981'],P=[50,14,30,3,3];
function vb(){const ok=Date.now()-S.w>=864e5,g=WC.concat(WC).map((c,i)=>`${c} ${i*36}deg ${i*36+36}deg`).join(','),link=`https://t.me/${BOT}?start=ref_${UID}`;
 $('main').innerHTML=`<div class="ru" style="font-size:26px;color:#ffe08a">КОЛЕСО УДАЧИ</div><div style="position:relative;margin:28px 0 8px"><div style="position:absolute;left:50%;top:-22px;margin-left:-16px;border-top:30px solid #ef4444;border-left:16px solid transparent;border-right:16px solid transparent;z-index:3"></div><div id="wh" style="background:conic-gradient(${g});transform:rotate(${cur}deg)">${Array.from({length:10},(_,k)=>`<span style="transform:rotate(${k*36+18}deg) translateY(-108px)">${W[k%5]}</span>`).join('')}</div></div><button class="b3 gold" onclick="wheel()" ${ok?'':'disabled'}>${ok?'КРУТИТЬ КОЛЕСО':'ЧЕРЕЗ <span id="wt"></span>'}</button>
 <div class="ru" style="font-size:20px;align-self:flex-start;margin:22px 0 8px">ЗАДАНИЯ ДНЯ <small style="font:12px Sora;color:#b9b0e0">новые через <span id="qt"></span></small></div>`+
 S.q.ids.map(id=>{const [d,t,k,n,r]=Q[id],p=Math.min(S.q.prog[k]||0,n),c=S.q.claimed[id];return `<div class="card"><div class="row"><span style="flex:1">${t}</span><button class="b3 gold sm" ${p>=n&&!c?'':'disabled'} onclick="claim(${id})">${c?'ГОТОВО':'+'+r+' ★'}</button></div><div class="bar"><i style="width:${p/n*100}%"></i></div><small>${fmt(p)} / ${fmt(n)}</small></div>`}).join('')+
 `<div class="card"><b class="ru">ДРУЗЬЯ</b><br><small style="word-break:break-all;color:#b9b0e0">${link}</small><div class="row" style="margin-top:8px"><button class="b3 gold sm" onclick="try{navigator.clipboard.writeText('${link}')}catch(e){};md('Ссылка скопирована')">КОПИРОВАТЬ</button><button class="b3 gr sm" onclick="share('Заходи в Car Roulette, выбивай крутые тачки!')">ПРИГЛАСИТЬ</button></div><small style="color:#b9b0e0">+10 ★ за друга начисляет сервер бота.</small></div>`}
async function wheel(){if(busy||Date.now()-S.w<864e5)return;busy=1;let x=Math.random()*100,t=0;for(;t<4;t++){x-=P[t];if(x<0)break}
 const k=t+5*(Math.random()*2|0);S.w=Date.now();save();cur=Math.ceil(cur/360)*360+1800-(k*36+18)+(Math.random()*20-10);
 const w=$('wh');w.style.transition='transform 5s cubic-bezier(.1,.7,.1,1)';w.style.transform=`rotate(${cur}deg)`;await sleep(5300);
 let h;if(t%2==0){const n=[5,0,10,0,50][t];S.s+=n;h=`<div class="ru" style="font-size:34px">★ +${n}</div>`}
 else{const ri=t==1?3:4,c=rnd(C[ri]);add(ri,c);if(ri==4)confetti();h=`<div style="font-size:60px">${E[ri]}</div><b class="ru" style="color:${R[ri].c}">${R[ri].n}</b><br>${c[0]}<br><span class="ru" style="color:#ffe08a">${fmt(c[1]*1e3)} ₽</span>`}
 tr('wheel');bal();busy=0;vb();md(h)}
function claim(id){S.s+=Q[id][4];S.q.claimed[id]=1;bal();save();vb()}
// ---- Магазин ----
function vm(){$('main').innerHTML='<div class="ru" style="font-size:26px;align-self:flex-start">МАГАЗИН</div><p style="color:#b9b0e0;margin:4px 0 12px;align-self:flex-start">Игровые ★ за Telegram Stars</p>'+[50,100,300,500,1000].map(n=>`<div class="card row"><span class="coin">★</span><b class="ru" style="flex:1;font-size:20px">${n}</b><button class="b3 gold sm" onclick="md('Оплата Telegram Stars работает только через сервер бота (invoice и successful_payment). В этой версии покупка недоступна.')">${n} Stars</button></div>`).join('')}
// ---- Таймеры ----
function tick(){if(today()!=S.q.day){newDay();if(T==3&&!busy)vb()}const m=Date.now()+108e5,l=Math.ceil(m/864e5)*864e5-m,f=ms=>new Date(ms).toISOString().slice(11,19),a=$('qt');if(a)a.textContent=f(l);const w=$('wt');if(w){const r=864e5-(Date.now()-S.w);if(r<=0&&!busy)vb();else w.textContent=f(r)}}
if(S.q.day!=today())newDay();bal();go(0);setInterval(tick,1000);
</script></body></html>
