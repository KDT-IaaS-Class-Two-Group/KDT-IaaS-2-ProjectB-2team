import React from "react";

const Predict: React.FC  = () => {
  return (
    <div id="root">
      <div>사망보고서</div>
      <div>능력치
        <div>이미지</div>
        <div>
          <div>
            <div> 
              <div>닉네임</div>
              <div>지역</div>
            </div>
            <div>
              <div>능력치</div>
              <div>
                <div>hp</div>
                <div>공격력</div>
                <div>방어력</div>
                <div>정확도</div>
                <div>민첩성</div>
                <div>무게</div>
              </div>
            </div>
          </div>
          <div>10일</div>
        </div>
      </div>
      <div>사망이력</div>
      <div>메인 글 
        <div></div> {/*메인 글은 동적으로 생되게 만들기 */}
      </div>
      <div>버튼</div>
      <div>다음 페이지?</div>
    </div> 
  )
}
export default Predict