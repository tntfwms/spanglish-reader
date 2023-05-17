

function showSpanishWord(word){
    var el = document.getElementById(`spanish-word-${word}`);
    if (el === null){
        var info = data[word];
        var el = document.createElement('div');
        el.id = `spanish-word-${word}`;
        el.className = 'background';
        el.style.position = 'fixed';
        el.style.top = '0';
        el.style.right = '0';
        el.style.bottom = '0';
        el.style.left = '0';
        el.onclick = function(){hideSpanishWord(word);};
        el.style.zIndex = '9999';
        document.body.appendChild(el);
        
        const div = document.createElement('div');
        div.style.color = 'white';
        el.appendChild(div);

        const wordEl = document.createElement('h1');
        const wordAEl = document.createElement('a');
        wordAEl.href = info.url;
        wordAEl.innerText = word;
        div.appendChild(wordEl);
        wordEl.appendChild(wordAEl)

        const hrEl = document.createElement('hr');
        div.appendChild(hrEl);

        const defEl = document.createElement('h3');
        const defAEl = document.createElement('a');
        defAEl.href = info.def_url;
        defAEl.target = '__blank';
        defAEl.innerText = info.text;
        defEl.appendChild(defAEl)
        div.appendChild(defEl);


        const style = `
        .background {
            background-color: rgba(0, 0, 0, 0.7);
        }
        
        .background > div {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 10000;
            background-color: rgb(14, 1, 72);
            width: 20%;
            height: 20%;
            border-radius: 20px;
            text-align: center;
        }
        
        .background a {
            color: inherit;
            text-decoration: none;
        }
        .background a:hover {
            text-decoration: underline
        }
        `;
    
        const styleSheet = document.createElement('style');
        styleSheet.innerText = style;
        el.appendChild(styleSheet);
    } else {
        el.style.display = 'block';
    }
}

function hideSpanishWord(word){
    var el = document.getElementById(`spanish-word-${word}`);
    el.style.display = 'none';
}

function startLoading() {
    const overlay = document.createElement('div');
    overlay.className = 'loading';
    overlay.id = 'loading-screen';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.right = '0';
    overlay.style.bottom = '0';
    overlay.style.left = '0';
    overlay.style.zIndex = '9999';
    document.body.appendChild(overlay);
  
    const loadingDiv = document.createElement('div');
    overlay.appendChild(loadingDiv);
  
    const loadingIcon = document.createElement('div');
    loadingIcon.className = 'loading-icon';
    loadingDiv.appendChild(loadingIcon);
  
    const style = `
      .loading {
      background-color: rgba(0, 0, 0, 0.7);
      }
  
      .loading > div {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 10000;
      }
  
      .loading > div > .loading-icon {
      border: 16px solid #f3f3f3;
      border-radius: 50%;
      border-top: 16px solid #3498db;
      width: 120px;
      height: 120px;
      -webkit-animation: spin 2s linear infinite;
      animation: spin 2s linear infinite;
      background-color: black;
      position: relative;
      margin: auto;
      }
  
      /* Safari */
      @-webkit-keyframes spin {
      0% {
          -webkit-transform: rotate(0deg);
      }
      100% {
          -webkit-transform: rotate(360deg);
      }
      }
  
      @keyframes spin {
      0% {
          transform: rotate(0deg);
      }
      100% {
          transform: rotate(360deg);
      }
    `;
  
    const styleSheet = document.createElement('style');
    styleSheet.innerText = style;
    overlay.appendChild(styleSheet);
  }
  
  function stopLoading(){
      let loadingDiv = document.getElementById('loading-screen');
      document.body.removeChild(loadingDiv);
  }