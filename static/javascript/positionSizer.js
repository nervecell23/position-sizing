(function(exports){

  function PositionSizer(){



  }

  PositionSizer.calculateAtrBasedPs = function(atr, totalBalanceGbp, gbpusd){
    return totalBalanceGbp * gbpusd * 0.03 / (atr * 2 * 0.0001);
  }

  exports.PositionSizer = PositionSizer;

})(this)
