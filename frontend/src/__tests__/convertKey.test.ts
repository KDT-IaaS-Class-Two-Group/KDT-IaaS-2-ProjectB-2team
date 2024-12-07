import convertKey from "../modules/convertKey";

const mockStatTable = {
  species: "종족",
  attack: "공격력",
  defense: "방어력",
  accuracy: "정확도",
  weight: "체중",
};

describe("convertKey", () => {
  it("should return the correct mapped value for a known key", () => {
    expect(convertKey("species", mockStatTable)).toBe("종족");
    expect(convertKey("attack", mockStatTable)).toBe("공격력");
    expect(convertKey("defense", mockStatTable)).toBe("방어력");
    expect(convertKey("accuracy", mockStatTable)).toBe("정확도");
    expect(convertKey("weight", mockStatTable)).toBe("체중");
  });

  it("should return the original key if it is not in statTable", () => {
    expect(convertKey("unknownKey", mockStatTable)).toBe("unknownKey");
    expect(convertKey("randomKey", mockStatTable)).toBe("randomKey");
  });
});