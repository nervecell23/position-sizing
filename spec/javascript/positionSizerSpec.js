describe("PositionSizer", ()=>{

  describe("#calculateAtrBasedPs", ()=>{
    it("calculates position size based on ATR", ()=>{
      subject = PositionSizer.calculateAtrBasedPs(25, 10000, 1.23);
      expect(subject).toEqual(73800);
    })
  })

})
