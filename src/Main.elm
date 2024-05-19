module Main exposing (Model, Msg(..), init, main, subscriptions, update, view, viewLink)

import Browser
import Browser.Navigation as Nav
import Html exposing (..)
import Html.Attributes exposing (..)
import Url



--
--
-- MAIN
--
--


main : Program () Model Msg
main =
    Browser.application
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        , onUrlChange = UrlChanged
        , onUrlRequest = LinkClicked
        }



--
--
-- MODEL
--
--


type alias Model =
    { key : Nav.Key
    , url : Url.Url
    , authed : IsAuthed
    }


init : () -> Url.Url -> Nav.Key -> ( Model, Cmd Msg )
init flags url key =
    ( Model key url False, Cmd.none )


urls : List String
urls =
    [ "Home", "About", "Books", "Profile", "Contact" ]



{- Is the user logged into the site? -}


type IsAuthed
    = True
    | False



--
--
-- UPDATE
--
--


type Msg
    = LinkClicked Browser.UrlRequest
    | UrlChanged Url.Url


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        LinkClicked urlRequest ->
            case urlRequest of
                Browser.Internal url ->
                    ( model, Nav.pushUrl model.key (Url.toString url) )

                Browser.External href ->
                    ( model, Nav.load href )

        UrlChanged url ->
            ( { model | url = url }
            , Cmd.none
            )



--
--
-- SUBSCRIPTIONS
--
--


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none



--
--
-- VIEW
--
--


view : Model -> Browser.Document Msg
view model =
    { title = "Sigrid Undset Fangirls"
    , body =
        toolbar False
            |> List.append [ br [] [] ]
            |> List.append [ div [] [ getMainContent model ] ]
            |> List.reverse
    }



{-
   Defines what our toolbar/titlebar is going to look like.
-}


toolbar : IsAuthed -> List (Html msg)
toolbar isAuthed =
    [ h1 [ style "background-color" "gray" ] [ text "Sigrid Undset Fangirls" ]
    , tr [ style "background-color" "gray" ] (List.map viewLink urls)
    ]



{-
   Helper for creating table cells with links in them.
-}


viewLink : String -> Html msg
viewLink path =
    td [] [ a [ href ("/" ++ path) ] [ text (path ++ " | ") ] ]



{-
   Switch for main content in the webpage.
-}


getMainContent : Model -> Html msg
getMainContent model =
    case model.url.path of
        "/" ->
            text "i am root"

        "/Home" ->
            text "cat"

        "/About" ->
            text "aboot"

        "/Books" ->
            text "boeks"

        "/Profile" ->
            text "rpofa"

        "/Contact" ->
            text "Hey you can report a bug here"

        _ ->
            text "wtf this is undefined paeg"
