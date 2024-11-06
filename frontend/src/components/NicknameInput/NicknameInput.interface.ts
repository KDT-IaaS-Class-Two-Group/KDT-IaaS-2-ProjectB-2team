import React from "react";

export interface NicknameInputProps {
  inputRef: React.RefObject<HTMLInputElement>;
  changehandler?: React.ChangeEventHandler
}