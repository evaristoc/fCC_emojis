if (!d3.charts) {
    d3.charts = {};
};

d3.charts.table = function module(){
    //private variables, defaults values, and dispatchers
    var table;
    //exports
    function exports(_selection) {
      _selection.each(function(_data){
            //definition of basic layouts
        
            //instantiation of the displaying canvas
            if (!table) {
                table = d3.select(this).append('table').classed('emoji-table',true)
            }
            //instantiation of basic layouts
            var row = table.selectAll('tr.emoji-row').data(_data)
            
            //enter (if no table showing yet, create one)
            var rowEnter = row.select('tr').classed('emoji-row', true)
            
            //update (if table, change it)
            
            //exit (get rid of deleted elements)
           
        })  
    }
    //external bindings (getters / setters)
    
    //returning the function
    return exports
}