import { ISubmitData } from "@/shared/interface/data.interface";
import { IResultData } from "@/shared/interface/data.interface";

export interface IUserContext extends IResultData, ISubmitData {}

export interface UserContextType {
  userData: IUserContext | null;
  setUserData : (result : IUserContext | null)=> void
}