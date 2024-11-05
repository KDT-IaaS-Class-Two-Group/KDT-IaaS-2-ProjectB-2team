import { NicknameInputProps } from "./NicknameInput.interface"


const NicknameInput : React.FC<NicknameInputProps> = ({inputRef})=>{
  return(
  <div className="mb-4 bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont text-[#C5C1C3] flex">
  <p>닉네임 :</p>
  <input
    type="text"
    ref={inputRef}
    placeholder="닉네임을 입력하세요"
    className="bg-[#332F47CC] text-[#C5C1C3] text-lg placeholder-white ml-2"
  />
</div>
  )
}

export default NicknameInput