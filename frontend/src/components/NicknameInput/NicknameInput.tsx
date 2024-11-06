import { NicknameInputProps } from "./NicknameInput.interface";

const NicknameInput: React.FC<NicknameInputProps> = ({ inputRef, changehandler }) => {
  return (
    <div className="w-full flex items-center sm:justify-start bg-[#332F47CC] rounded border border-[#D9C4B2] font-cfont text-[#C5C1C3]">
      <label htmlFor="nickname" className="whitespace-nowrap mr-2">닉네임 :</label>
      <input
        id="nickname"
        type="text"
        ref={inputRef}
        onChange={changehandler}
        placeholder="닉네임을 입력하세요"
        className="w-full bg-[#332F47CC] text-[#C5C1C3] sm:text-lg placeholder-white flex-1 overflow-hidden text-ellipsis whitespace-nowrap input"
        autoComplete="off"
        name="username"
      />
    </div>
  );
};

export default NicknameInput;