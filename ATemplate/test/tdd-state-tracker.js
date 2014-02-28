var TDDStates = {
    test: {className: "tddstate-test", desc:"Develop failing unit test (not compiling is also failing)", fail: "implement", success: "test"},
    implement: {className: "tddstate-implement", desc:"Write code that makes unit test pass (but no more)", fail: "implement", success:"refactor"},
    refactor:{className: "tddstate-refactor", desc:"Refactor code while making sure that unit tests stay green", fail: "refactor", success:"test"},
};

function changeStateElement(stateElement, newState) {
    var stateObject = TDDStates[newState];
    stateElement.attr("class", stateObject.className);
    stateElement.text(stateObject.desc);
}
function TDDStateTracker(stateElement,unitTestCheck,store) {
	this.unitTestCheck=unitTestCheck;
	this.stateElement=stateElement;
    this.store=store;
    this.initState=function() {
        if (this.store && this.store.TDDState) {
            this.currentState=this.store.TDDState;
        } else {
            this.currentState=this.unitTestCheck()?"test":"implement";
        }
		changeStateElement(this.stateElement, this.currentState);
        return TDDStates[this.currentState];
    };
	this.update=function() {
        if (this.timestamper) {
            $.get(this.timestamper,function () {});
        }
		if (this.unitTestCheck()) {
			this.currentState=TDDStates[this.currentState].success
		} else {
			this.currentState=TDDStates[this.currentState].fail
		}
        if (this.store) {
            this.store.TDDState=this.currentState;
        }
        changeStateElement(this.stateElement, this.currentState);
		return TDDStates[this.currentState];
	};
	this.current_time=function() {
		return Math.floor(new Date().getTime()/1000);
	};
	this.get_cycle_time=function () {
		var time_delta;
		var timestamp=this.current_time();
		if (this.store.timestamp) {
			time_delta=timestamp-this.store.timestamp
		} else {
			time_delta=0;
		}
		this.store.timestamp=timestamp;
		return time_delta;
	};
    this.update_cycle_time=function () {
        var cycle_time=this.get_cycle_time();
        var count=this.store.cycles;
        var average=this.store.average;
        if (cycle_time>0) {
            if (average>0) {
                if (count>0) {
                    average=(count*average+cycle_time)/(count+1)
                } else {
                    average=(average+cycle_time)/2
                };
                count++;
            } else {
                average=cycle_time;
                count=1;
            };
            var old_text=this.stateElement.text();
            if (old_text != "" ) {
                old_text += " ";
            };
            this.stateElement.text(old_text+"(latest cycle: "+cycle_time+" seconds, average: "+average+" seconds)");
            this.store.cycles=count;
            this.store.average=average;
        }
    }
    this.update_with_cycle_time=function(cycleState) {
        var previousState=this.currentState;
        this.update();
        if (this.currentState==cycleState && previousState != this.currentState) {
            this.update_cycle_time();
        }
    }
};
