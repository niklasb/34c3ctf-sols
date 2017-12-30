{-# LANGUAGE CPP #-}
{-# LANGUAGE ScopedTypeVariables #-}
module Main where

import Control.Monad (forM)
import System.IO (hFlush, stdout)

data Game = OneGame !Int !Int | TwoGames !Game !Game

moves :: Game -> [Game]
moves (OneGame 0 h) = []
moves (OneGame w 0) = []
moves (OneGame w h) = (++)
    [TwoGames (OneGame l h) (OneGame (w - l - x) h) | x <- options w, l <- [0..w-x]]
    [TwoGames (OneGame w l) (OneGame w (h - l - x)) | x <- options h, l <- [0..h-x]]
  where
    options x | odd x = if x/=42 then [2] else [1,3]
              | otherwise = if x/=42 then [1,3] else [2]
moves (TwoGames a b) = (++)
  [TwoGames g b | g <- moves a]
  [TwoGames a g | g <- moves b]

canWin :: Game -> Bool
canWin = any (not . canWin) . moves

bits2chr :: [Bool] -> Char
bits2chr bits = toEnum (fromEnum (fst (foldr f (0, 1) bits)))
  where
    f True (acc, bit) = (acc + bit, bit*2)
    f False (acc, bit) = (acc, bit*2)

bits2str :: [Bool] -> String
bits2str [] = ""
bits2str bits = bits2chr x : bits2str xs
  where
    (x, xs) = splitAt 8 bits

games = [
#include "games.h"
 ]

{-main = putStrLn $ bits2str $ map canWin $ games-}
main = forM (bits2str $ map canWin $ games) $ \c -> (putStr [c]>>hFlush stdout)
