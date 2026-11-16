(function(){
const Q="['‘’ʻʼ`´′]";
const fwd=s=>{let n=0;
s=s.replace(new RegExp("([OoGg])"+Q,"g"),(m,c)=>{n++;return {O:"Ö",o:"ö",G:"Ğ",g:"ğ"}[c]});
s=s.replace(/([Ss])[Hh]/g,(m,c)=>{n++;return c=="S"?"Ş":"ş"});
s=s.replace(/([Cc])[Hh]/g,(m,c)=>{n++;return c=="C"?"Ç":"ç"});
return [s,n]};
const M={"Ö":"O‘","ö":"o‘","Ğ":"G‘","ğ":"g‘","Ş":"Sh","ş":"sh","Ç":"Ch","ç":"ch"};
const rev=s=>{let n=0;s=s.replace(/[ÖöĞğŞşÇç]/g,m=>{n++;return M[m]});return [s,n]};
const CY=/[А-Яа-яЁёЎўҚқҒғҲҳ]/g,CL=/[А-Яа-яЁёЎўҚқҒғҲҳ]/,VW=/[аеёиоуўэюяыАЕЁИОУЎЭЮЯЫ]/;
const C={а:"a",б:"b",в:"v",г:"g",д:"d",ж:"j",з:"z",и:"i",й:"y",к:"k",л:"l",м:"m",н:"n",о:"o",п:"p",р:"r",с:"s",т:"t",у:"u",ф:"f",х:"x",ц:"ts",ч:"ch",ш:"sh",щ:"shch",ъ:"’",ь:"",ы:"i",э:"e",ю:"yu",я:"ya",ё:"yo",ў:"o‘",қ:"q",ғ:"g‘",ҳ:"h",е:"e"};
const B={a:"а",b:"б",d:"д",f:"ф",g:"г",h:"ҳ",i:"и",j:"ж",k:"к",l:"л",m:"м",n:"н",o:"о",p:"п",q:"қ",r:"р",s:"с",t:"т",u:"у",v:"в",x:"х",y:"й",z:"з"};
const up=c=>c!==c.toLowerCase(),ap=c=>!!c&&/['‘’ʻʼ`´′]/.test(c),cap=(m,all)=>all?m.toUpperCase():m[0].toUpperCase()+m.slice(1);
function cyr2lat(s){return s.replace(CY,(c,i)=>{const l=c.toLowerCase(),p=s[i-1],n=s[i+1];let m=C[l];
if(l=="е")m=(!p||!CL.test(p)||VW.test(p))?"ye":"e";
if(l=="ц"&&(!p||!CL.test(p)))m="s";
if(!up(c)||!m)return m;
return cap(m,m.length>1&&((n&&CL.test(n)&&up(n))||(p&&CL.test(p)&&up(p))))})}
function lat2cyr(s){let o="";for(let i=0;i<s.length;){const c=s[i],l=c.toLowerCase(),n=s[i+1]||"",nl=n.toLowerCase();let m,len=1;
if((l=="o"||l=="g")&&ap(n)){m=l=="o"?"ў":"ғ";len=2}
else if(l=="s"&&nl=="h"){m="ш";len=2}
else if(l=="c"&&nl=="h"){m="ч";len=2}
else if(l=="t"&&nl=="s"){m="ц";len=2}
else if(l=="y"&&nl&&"ouae".includes(nl)&&!(nl=="o"&&ap(s[i+2]))){m={o:"ё",u:"ю",a:"я",e:"е"}[nl];len=2}
else if(ap(c))m="ъ";
else if(l=="e")m=(i&&/[a-z‘’ʻʼ'`´′]/i.test(s[i-1]))?"е":"э";
else m=B[l];
if(!m){o+=c;i++;continue}
if(up(c))m=cap(m,len==2&&up(n)&&m.length>1);
o+=m;i+=len}return o}
const toOld={o:s=>[s,0],n:rev,c:s=>[cyr2lat(s),0]};
const fromOld={o:s=>[s,0],n:fwd,c:s=>[lat2cyr(s),0]};
const UZ=window.UZ={};
UZ.conv=(s,f,t)=>f==t?s:fromOld[t](toOld[f](s)[0])[0];
// Word hujjatidagi matnni so‘zma-so‘z almashtiradi (formatlash saqlanadi).
// scope: "sel" = tanlangan matn (tanlanmagan bo‘lsa butun hujjat), "all" = butun hujjat
UZ.run=async(f,t,scope)=>{
let n=0,used="hujjat";
await Word.run(async ctx=>{
let src=ctx.document.body;
if(scope!="all"){const sel=ctx.document.getSelection();sel.load("text");await ctx.sync();if(sel.text&&sel.text.trim()){src=sel;used="tanlangan matn"}}
const rs=src.getTextRanges([" "],false);rs.load("items/text");await ctx.sync();
for(let i=0;i<rs.items.length;i+=400){
rs.items.slice(i,i+400).forEach(r=>{const x=UZ.conv(r.text,f,t);if(x!==r.text){r.insertText(x,"Replace");n++}});
await ctx.sync()}
});
return {n:n,used:used}};
})();
