import urllib2
import re

house_year = {
"gy1": "modestovalde, huifen, suklee, mtlee, kiewjs, howboonseng, chuaszemin, jdomingo",
"gy2": "yanghao, mdantiochia, kongmin, jrmalics, derzhan, choonhian, hanny, hanjian",
"gy3": "lixin, chengshua, tkoh, rsumaputra, lrdeguzm, nyetyun, etseah, karthiks",
"gy4": "vguillermo, ahsia, weekiat, rbmacabi, anqin, joannlee, raymondang, clorenz",
"hy1": "teckyeelim, ravins, chuakc, rogerhor, ngcw, manakdunggau, hychong, ehgan",
"hy2": "allee, limkl, yewmeng, bcchiam, rajjul, jglim, ysgoh, grajasekar, jiajun",
"hy3": "gordonchin, kctong, yshong, lchung, jsmedina, christinecky, yping, honpeiling, boonpin",
"hy4": "tanchiayng, imkeh, khoosianyong, empeleo, jdsolomo, lamsoonleong, evanter, pohhong",
"ry1": "kchia, louisegohth, chinhoi, kienhan, cranchores, christinelis, wongshihnern, petersee",
"ry2": "andychowlt, klai, ahmadmazhar, ggerard, joycetuge, liyan, soonyee, sengyew",
"ry3": "laimei, teheexyan, tmkoh, bennyong, yixuan, anila, rachmatw, eileentanyl, siangleong",
"ry4": "oeg, cgarcia, tanchunseng, mongsoon, siaufen, carlineteh, kianchai, ckyew",
"sy1": "amyloi, simonlai, pgdelac, cheekheng, cheehau, boonzhiu, jamestacata, cheauhuey",
"sy2": "kcheng, hanjiong, chewkorkiat, seahyc, tankkiang, jefferykong, balakumaranr, kahweng, tazumi",
"sy3": "mccolina, fong, huaiseng, linglili, slkl, thyeo, scydesmond, vernonlim, dhika",
"sy4": "tankai, leongkw, jlgaray, ranganathan, yeewan, zhanghong, stanleylai, xiaowen",
}

#call("98371397", {"network":"SMS"})
if currentCall.initialText==None:
   msg = "house tankokhua"
else:
   msg = currentCall.initialText.strip().lower()

orig_msg = msg
msg = msg.replace(' ', '%20')
url = "http://wizardry-tournament.appspot.com/sms?message=%s&caller=%s" % (msg, currentCall.callerID)
resp=urllib2.urlopen(url)
reply = resp.read()

if reply!="0":
   if msg.startswith("whatsapp"):
      say(reply)
      message(reply, {"to":"98371397",   "network":"SMS"})
   elif msg.startswith("house"):
      if re.search(r'Year (\d)( Team Leader)? of (Slytherin|Gryffindor|Hufflepuff|Ravenclaw)', reply):
         results = re.search(r'Year (\d)( Team Leader)? of (Slytherin|Gryffindor|Hufflepuff|Ravenclaw)', reply).groups()
         if results:
            group = results[2][0].lower()+'y'+results[0]
            if house_year.get(group, None):
               reply += " [" + house_year.get(group) + "]"
      say(reply)
else:
   say("Invalid input. Please try again.")
