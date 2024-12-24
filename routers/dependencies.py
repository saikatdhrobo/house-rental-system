from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

import models, schemas
from database import get_db