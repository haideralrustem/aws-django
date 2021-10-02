console.log('this is project2 js')
var window_media_query_offset = 17;

// let parsed_data = null;
// parsed_data = JSON.parse('{{json_recieved_data|safe}}')

var colorsArray = ["#10ac84", "#54a0ff", "#ff9f43", 
                       "#7d5fff", "#c56cf0", "#ffb8b8",
                       "#6D214F", 
                        ];

var selectedWords = [];
var selectedColors = [];




function wordFreq(data, w=460, h=400, fontSize="14px") {
        // set the dimensions and margins of the graph
    var margin = {top: 10, right: 10, bottom: 80, left: 100},

    width = w - margin.left - margin.right,
    
    height = h - margin.top - margin.bottom;

    let max_ticks = data[0]['count'];

    

    d3.select("#my_dataviz svg").remove();

    // append the svg object to the body of the page
    var svg = d3.select("#my_dataviz")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        
        .attr("height", height + margin.top + margin.bottom)
        
        .attr("class", ".my_dataviz")
       
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

      
        // Add X axis
        var x = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return d.count; })])
        .range([ 0, width]);
        svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        // .call(d3.axisBottom(x).tickFormat(d3.format("d")).ticks((data.length)-1) )
        .call(d3.axisBottom(x).ticks(max_ticks) )
        
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        
        .style("text-anchor", "end")
        .style("font-size", fontSize);

        // Y axis
        var y = d3.scaleBand()
        .range([ 0, height ])
        .domain(data.map(function(d) { return d.word; }))
        .padding(.1);

        svg.append("g")
        .call(d3.axisLeft(y))
        .selectAll("text")
        .attr("class", "plot-word")
        .style("font-size", fontSize)
        ;


        //Bars
        svg.selectAll("myRect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", x(0) )
        .attr("y", function(d) { return y(d.word); })
        .attr("width", function(d) { return x(d.count); })
        .attr("height", y.bandwidth() )
        
        .attr("fill", function (d, i){ return colorsArray[i]; });
        

        document.querySelectorAll('.plot-word').forEach(
            function(item, i) {
            
            item.addEventListener('click', function(event) {
                event.stopPropagation();
              //handle click
              clickPlotWord(this, i);
            })
          });


          function clickPlotWord(clickedItem, colorNumber) {
            console.log('clicked item => ', clickedItem.innerHTML);
            if ($(clickedItem).hasClass('plot-word-selected'+colorNumber)){
                $(clickedItem).removeClass('plot-word-selected'+colorNumber);
                
                // unhighlight text
                if ( selectedWords.includes(selectedWord)) {
                    const index = selectedWords.indexOf(selectedWord);
                    array.splice(index, 1);
                }
                if ( selectedColors.includes(colorNumber)) {
                    const index = selectedColors.indexOf(colorNumber);
                    array.splice(index, 1);
                }

            }
            else {
                $(clickedItem).addClass('plot-word-selected'+colorNumber);
                // highlight text
                //highlightWordsTextArea(clickedItem.innerHTML);
                let selectedWord = clickedItem.innerHTML;
                if ( ! selectedWords.includes(selectedWord)) {
                    selectedWords.push(selectedWord);
                }
                if ( ! selectedColors.includes(colorNumber)) {
                    selectedColors.push(colorNumber);
                }
                initiateTextAreaOverlayProps(selectedWords, selectedColors);
            }
           

          }

          

}




// set the values of overlay so that its identitcal to the textarea
function initiateTextAreaOverlayProps(selectedWords, selectedColors) {
    console.log("  initiateTextAreaOverlayProps() was called ! \n");
    // set text

    //set css
    //margin: 0% 0 0 3%;

    // selectedWord = 'vaccination';
    
    

    let tx =  $("#txa_textarea").val().replace(/\n/g, "<br />");

    selectedWords.forEach(function(selectedWord, i) {
        let re = new RegExp(selectedWord, "g");
        let colorNumber = selectedColors[i];
        let highlightedSelectedWord = `<span class="highlighter highlighted-textarea-word${colorNumber}">${selectedWord}</span>`
        let fs = $("#txa_textarea").css("font-size");
        let margin = $("#txa_textarea").css("margin");
        let padding = $("#txa_textarea").css("padding");
        let border = $("#txa_textarea").css("border");
    
        $(".highlight-overlay").css(
            {
            "font-size": fs,
            // "border": border,
            });

        tx = tx.replace(re, highlightedSelectedWord);
    });   

    console.log(tx);

    $('.highlight-overlay').html(tx);
    
    $("#txa_textarea").scrollTop(0);

    // now match the scrolling pattern
    let target = $(".highlight-overlay")[0];
    $("#txa_textarea").scroll(function() {
        target.scrollTop = this.scrollTop;
             
    });

    

    // responisveness
    // color coding

}


function removeOverlay() {
   
    let classNumbers = [0, 1, 2, 3, 4, 5, 6]
    let classSelector = `.highlighter`;

    

    $( classSelector ).each(function( index ) {
        let elem = $(this);

        classNumbers.forEach(function(classNumber, i) {
        
            let classForRemoval = `highlighted-textarea-word${classNumber}`
            
            $(elem).removeClass(classForRemoval);
        });
      
    });

    selectedWords = [];
    selectedColors = [];

}   


function finalHighlighter(listOfSelectedWords) {

    listOfSelectedWords
}

function adjustTextAreaOverlay() {

}


function highlightWords() {
    $(".highlight-overlay").width ($('#txa_textarea').width());
    $(".highlight-overlay").height ($('#txa_textarea').height());
    let highlight_overlay = document.querySelector('.highlight-overlay');

    let txtarea = document.querySelector('#txa_textarea');
    let coords_offset = getOffset(highlight_overlay);
    
    console.log(coords_offset);
    console.log(getOffset(txtarea));
    highlight_overlay

    initiateTextAreaOverlayProps();
  }


window.addEventListener('resize', function(event) {
    // textAreaOverlayOnResize();    
    }, true);


// ........................


function textAreaOverlayOnResize() {
    let highlightOverly = document.querySelector('.highlight-overlay');
    let textArea = document.querySelector('.txa_textarea');

    highlightOverly.style.width = textArea.offsetWidth + "px";
}



function getOffset(el) {
    const rect = el.getBoundingClientRect();
    return {
      left: rect.left + window.scrollX,
      top: rect.top + window.scrollY
    };
  }


function highlightWordsTextArea(highlightedWord) {
    let textArea = document.getElementById("txa_textarea");
    let text = textArea.value;
    let newText = "";
    let wrappedWord = `<span class='highlighted-textarea-word'>${highlightedWord}</span>`
    newText = text.replace(highlightedWord, wrappedWord);
    textArea.nodeValue  = newText;
}



// a function when body clicks occur and we need to have a de-click
function declicker(){

    
    document.getElementById('text-analyzer-wapper').addEventListener('click',
        function(){

            // (1)
            document.querySelectorAll('.plot-word').forEach(
                function(item) {

                    colorsArray.forEach(function(color, index){

                        if ($(item).hasClass('plot-word-selected'+index)){
                            $(item).removeClass('plot-word-selected'+index);
                        }
                    });
                   
            });

            // 2 -
            removeOverlay()

            // 3 - 


        }
        
    );  

}

// execute function calls
//initiateTextAreaOverlayProps();

declicker();


let data= [{word: 'Hello', 'count': 10},
            {word: 'Verbose', 'count': 25},
            {word: 'Peli', 'count': 5},
            {word: 'Jack', 'count': 90},
            {word: 'Ink', 'count': 60}]


// wordFreq(data);